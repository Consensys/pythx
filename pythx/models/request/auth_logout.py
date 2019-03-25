"""This module contains the AuthLogoutRequest domain model."""

import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema


class AuthLogoutRequest(BaseRequest):
    """Perform an API request that logs out the current user."""

    with open(resolve_schema(__file__, "auth-logout.json")) as sf:
        schema = json.load(sf)

    def __init__(self, global_: bool = False):
        self.global_ = global_

    @property
    def endpoint(self):
        """The API's logout endpoint.

        :return: A string denoting the logout endpoint without the host prefix
        """
        return "v1/auth/logout"

    @property
    def method(self):
        """The HTTP method to perform.

        :return: The uppercase HTTP method, e.g. "POST"
        """
        return "POST"

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

    @property
    def payload(self):
        """The request's payload data.

        :return: A Python dict to be serialized into JSON format and submitted to the endpoint.
        """
        return {}

    @classmethod
    def from_dict(cls, d: Dict):
        """Create the request domain model from a dict.

        This also validates the dict's schema and raises a :code:`RequestValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        return cls(global_=d["global"])

    def to_dict(self):
        """Serialize the request model to a Python dict.

        :return: A dict holding the request model data
        """
        d = {"global": self.global_}
        self.validate(d)
        return d
