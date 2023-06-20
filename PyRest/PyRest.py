from flask import Flask
from flask_cors import CORS
from PyRest.ApiEndpoint import ApiEndpoint, request
from PyRest.Sessions import SessionToken, RefreshToken, SessionManager
from PyRest.Exceptions import *

class PyRest:
    def __init__(self, name: str, secret_key: str, auth_method: callable | None, debug=False):
        self.flask = Flask(name)
        self.flask['SECRET_KEY'] = secret_key
        self.session_manager = SessionManager(secret_key)
        self.auth_method = auth_method
    
    def add_route(self, route: str, endpoint: ApiEndpoint, authRequired: bool):
        if not authRequired:
            @self.flask.route(route, methods=endpoint.get_methods())
            def _method():
                method_used = request.method
                return endpoint.method(method_used, request)
            return    
        
        #Auth is required
        @self.flask.route(route, methods=endpoint.get_methods())
        def _method_auth():
            if "Authorization" not in request.headers:
                return 401, {"error": "Authorization header not found"}
            
        
    def run(self, port=5000, host="0.0.0.0"):
        return