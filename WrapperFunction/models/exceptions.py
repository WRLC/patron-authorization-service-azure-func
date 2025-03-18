"""
    This module defines custom exceptions for the application.
"""


class MessageException(Exception):
    """
    Custom exception class for handling messages.
    """
    def __init__(self, code: int, message: str):
        self.code: int = code
        self.message: str = message


class SendException(Exception):
    """
    Custom exception class for handling send errors.
    """
    def __init__(self, code: int, body: str):
        self.code: int = code
        self.body: str = body
