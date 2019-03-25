"""This module contains the OASRequest domain model."""

from pythx.models.exceptions import RequestValidationError
from pythx.models.request.base import BaseRequest


class OASRequest(BaseRequest):
    """Perform an API request that gets the OpenAPI spec."""

    def __init__(self, mode="yaml"):
        if not mode in ("yaml", "html"):
            raise RequestValidationError("'mode' must be one of {html,yaml}")
        self.mode = mode

    @property
    def endpoint(self):
        """The API's OpenAPI spec endpoint.

        :return: A string denoting the OpenAPI endpoint without the host prefix
        """
        return "v1/openapi" + (".yaml" if self.mode == "yaml" else "")

    @property
    def method(self):
        """The HTTP method to perform.

        :return: The uppercase HTTP method, e.g. "POST"
        """
        return "GET"

    @property
    def payload(self):
        """The request's payload data.

        :return: A Python dict to be serialized into JSON format and submitted to the endpoint.
        """
        return {}

    @property
    def parameters(self):
        """Additional URL parameters

        :return: A dict (str -> str) instance mapping parameter name to parameter content
        """
        return {}

    @property
    def headers(self):
        """Additional request headers.

        :return: A dict (str -> str) instance mapping header name to header content
        """
        return {}

    @classmethod
    def from_dict(cls, d):
        """Create the request domain model from a dict.

        This also validates the dict's schema and raises a :code:`RequestValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        return cls()

    def to_dict(self):
        """Serialize the request model to a Python dict.

        :return: A dict holding the request model data
        """
        return {}
