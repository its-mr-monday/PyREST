
class PyRestException(Exception):
    # Base class for all exceptions
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class PyRestSessionException(PyRestException):
    def __init__(self, message):
        super().__init__(message)
        
