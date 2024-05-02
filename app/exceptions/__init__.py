class BaseException(Exception):
    def __init__(self, response_message: str | None):
        self.response_message = response_message


class UserNotFoundException(BaseException):
    pass


class ValidationException(BaseException):
    pass
