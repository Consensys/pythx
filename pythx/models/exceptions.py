"""This module contains exceptions raised by PythX."""


class PythXBaseException(Exception):
    """A base exception describing PythX-related errors."""
    pass


class ResponseValidationError(PythXBaseException):
    """A validation exception for API responses.

    This is usually raised when the validation of a response fails. Validation is
    executed during deserialization of responses. Often these are raised, because
    required keys are not present, or the API response could not be validated using
    the given JSON schema spec.
    """
    pass


class RequestValidationError(PythXBaseException):
    """A validation exception for API requests.

    This is usually raised when the validation of a request fails. Validation is
    executed during serialization of requests. Often these are raised, because
    required keys are not present, or the API request could not be validated using
    the given JSON schema spec.
    """
    pass


class PythXAPIError(PythXBaseException):
    """An exception denoting an API-related error.

    This is usually raised when the API takes too long to respond, or a response contains
    an HTTP status code that is not 200 OK. In this case, the exception is passed on to the
    developer. This should give them early warnings about malformed data on their side, or
    recover in case the API is not available or experiences some kind of error we cannot handle.
    """
    pass
