# Create custom exception class
class MessageException(Exception):
    def __init__(self, code: int, message: str):
        self.code: int = code
        self.message: str = message


# SendException class
class SendException(Exception):
    def __init__(self, code: int, body: str):
        self.code: int = code
        self.body: str = body
