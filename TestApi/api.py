from PyRest.ApiEndpoint import ApiEndpoint, request

class LoginEndpoint(ApiEndpoint):
    def __init__(self):
        self.super(["POST"])
        
    def method(self, method: str, request: request) -> tuple[int, dict | str]:
        if method != "POST":
            return 405, {"error": "Method not allowed"}
        
        