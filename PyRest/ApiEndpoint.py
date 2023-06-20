from flask import request

class ApiEndpoint:
    def __init__(self, methods: list[str]):
        #
        self.methods = methods
        
    def get_methods(self) -> list[str]:
        return self.methods
        
    def method(self, method: str, request: request) -> tuple[int, dict | str]:
        pass