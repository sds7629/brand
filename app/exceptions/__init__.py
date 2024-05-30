class BaseException(Exception):
    def __init__(self, response_message: str | None):
        self.response_message = response_message


class UserNotFoundException(BaseException):
    pass


class QnANotFoundException(BaseException):
    pass


class ItemNotFoundException(BaseException):
    pass


class OrderNotFoundException(BaseException):
    pass


class ValidationException(BaseException):
    pass


class QnAValidationException(BaseException):
    pass


class NotPermissionException(BaseException):
    pass


class NoContentException(BaseException):
    pass
