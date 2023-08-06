from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi import FastAPI,Depends,Response,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.datastructures import MutableHeaders
import time
import json
from sixth import schemas
import re
import requests
from dotenv import load_dotenv
import os
import ast


class SixRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, apikey: str, fastapi_app: FastAPI, project_config: schemas.ProjectConfig):
        super().__init__(app)
        self._config = project_config
        self._log_dict = {}
        self._app = app
        self._apikey = apikey
        self._route_last_updated = {}
        for route in fastapi_app.router.routes:
            if type(route.app )== FastAPI:
                for new_route in route.app.routes:
                    path = "/v"+str(route.app.version)+new_route.path
                    edited_route = re.sub(r'\W+', '~', path)
                    self._log_dict[str(edited_route)] = {}
                    self._route_last_updated[str(edited_route)] = time.time()
            else:
                edited_route = re.sub(r'\W+', '~', route.path)
                self._log_dict[str(edited_route)] = {}
                self._route_last_updated[str(edited_route)] = time.time()
                

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}
        request._receive = receive
        
    def _is_rate_limit_reached(self, uid, route):
        timestamp = time.time()
        requests = self._log_dict[route].get(uid, None)
        rate_limit = self._config.rate_limiter[route].rate_limit
        interval = self._config.rate_limiter[route].interval
        if requests == None:
            self._log_dict[route][uid] = []
        if len(self._log_dict[route].get(uid)) < rate_limit:
            self._log_dict[route].get(uid, []).append(timestamp)
            return True
            
        new_req = [new_req for new_req in self._log_dict[route][uid] if new_req > timestamp-interval]
        if len(new_req) < rate_limit:
            self._log_dict[route][uid].append(timestamp)
            return True
        else: 
            return False
        
    async def _parse_bools(self, string: bytes)-> str:
        '''
            used  to parse boolean values in string format and convert it to Python's boolean format
        '''
        string = string.decode("utf-8")
        string = string.replace(' ', "")
        string = string.replace('true,', "True,")
        string = string.replace(",true", "True,")
        string = string.replace('false,', "False,")
        string = string.replace(",false", "False,")
        out=ast.literal_eval(string)
        return out
        
    async def dispatch(self,request: Request,call_next) -> None:
        host = request.client.host
        route = request.scope["path"]
        route = re.sub(r'\W+', '~', route)
        headers = request.headers
        query_params = request.query_params
        rate_limit_resp = None
        status_code = 200
        
        
        #fail safe if there is an internal server error our servers are currenly in maintnance
        try:
            if time.time() - self._route_last_updated[route] >5:
                #update rate limit details every 5 seconds
                rate_limit_resp = requests.get("https://backend.withsix.co/project-config/config/get-route-rate-limit/"+self._apikey+"/"+route)
                self._route_last_updated[route] = time.time()
                status_code = rate_limit_resp.status_code
            body = None

            try:
                body = await request.body()
                await self.set_body(request, body)
                body = await self._parse_bools(body)
            except:
                pass
            
            if status_code == 200: 
                try:
                    rate_limit = schemas.RateLimiter.model_validate(rate_limit_resp.json()) if rate_limit_resp != None else self._config.rate_limiter[route]
                    if rate_limit.is_active:
                        self._config.rate_limiter[route] = rate_limit
                        preferred_id = self._config.rate_limiter[route].unique_id
                    
                        if preferred_id == "" or preferred_id=="host":
                            preferred_id = host
                            
                        else:
                            if rate_limit.rate_limit_type == "body":
                                if body != None:
                                    preferred_id = body[preferred_id]
                                else:
                                    _response = await call_next(request)
                                    return _response
                            elif rate_limit.rate_limit_type == "header":
                                preferred_id = headers[preferred_id]
                            elif rate_limit.rate_limit_type == "args":
                                preferred_id = query_params[preferred_id]
                            else:
                                preferred_id = host
                        

                        if self._is_rate_limit_reached(preferred_id, route): 
                            _response = await call_next(request)
                            return _response
                        else:
                            temp_payload = rate_limit.error_payload.values()
                            final = {}
                            for c in temp_payload:
                                for keys in c:
                                    if keys != "uid":
                                        final[keys] = c[keys]
                            output= final
                            headers = MutableHeaders(headers={"content-length": str(len(str(output).encode())), 'content-type': 'application/json'})
                            return Response(json.dumps(output), status_code=420, headers=headers)
                    else:
                       
                        _response = await call_next(request)
                        return _response
                except Exception as e:
                   
                    _response = await call_next(request)
                    return _response
            else:
                #fail safe if there is an internal server error our servers are currenly in maintnance
                _response = await call_next(request)
                return _response
        except Exception as e:
            
            _response = await call_next(request)
            return _response