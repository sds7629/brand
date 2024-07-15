class BaseException(Exception):
    def __init__(self, response_message: str | None):
        self.response_message = response_message


class NoSuchContentException(BaseException):
    pass


class NoPermissionException(BaseException):
    pass


class NotFoundException(BaseException):
    pass


class QuantityException(BaseException):
    pass


class ValidationException(BaseException):
    pass


class AuthorizationException(BaseException):
    pass


class UserAlreadyExistException(BaseException):
    pass
