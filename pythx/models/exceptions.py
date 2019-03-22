class PythXBaseException(Exception):
    pass


class ResponseValidationError(PythXBaseException):
    pass


class RequestValidationError(PythXBaseException):
    pass


class PythXAPIError(PythXBaseException):
    pass
