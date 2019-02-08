class PythxBaseException(Exception):
    pass


class ResponseDecodeError(PythxBaseException):
    pass


class RequestDecodeError(PythxBaseException):
    pass


class RequestValidationError(PythxBaseException):
    pass
