class PythXBaseException(Exception):
    pass


class ResponseDecodeError(PythXBaseException):
    pass


class RequestDecodeError(PythXBaseException):
    pass


class RequestValidationError(PythXBaseException):
    pass


class PythXAPIError(PythXBaseException):
    pass
