class HTTPException(Exception):
    def __init__(self, code):
        self.code = code


class NotFound(HTTPException):
    def __init__(self):
        super().__init__(404)
