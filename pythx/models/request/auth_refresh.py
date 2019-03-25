"""This module contains the AuthRefreshRequest domain model."""

import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema


class AuthRefreshRequest(BaseRequest):
    """Perform an API request that refreshes the logged-in user's access token."""

    with open(resolve_schema(__file__, "auth-refresh.json")) as sf:
        schema = json.load(sf)

    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    def endpoint(self):
        """The API's auth refresh endpoint.

        :return: A string denoting the refresh endpoint without the host prefix
        """
        return "v1/auth/refresh"

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
        return {"accessToken": self.access_token, "refreshToken": self.refresh_token}

    @classmethod
    def from_dict(cls, d: Dict):
        """Create the request domain model from a dict.

        This also validates the dict's schema and raises a :code:`RequestValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_dict(self):
        """Serialize the request model to a Python dict.

        :return: A dict holding the request model data
        """
        d = {"access": self.access_token, "refresh": self.refresh_token}
        self.validate(d)
        return d
