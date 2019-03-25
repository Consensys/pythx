"""This module contains the AuthLoginRequest domain model."""

import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema

AUTH_LOGIN_KEYS = ("ethAddress", "password")


class AuthLoginRequest(BaseRequest):
    """Perform an API request that performs a login action with Ethereum address and password."""

    with open(resolve_schema(__file__, "auth-login.json")) as sf:
        schema = json.load(sf)

    def __init__(self, eth_address: str, password: str):
        self.eth_address = eth_address
        self.password = password

    @property
    def endpoint(self):
        """The API's login endpoint.

        :return: A string denoting the login endpoint without the host prefix
        """
        return "v1/auth/login"

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
        return self.to_dict()

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        """Create the request domain model from a dict.

        This also validates the dict's schema and raises a :code:`RequestValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        return cls(eth_address=d["ethAddress"], password=d["password"])

    def to_dict(self):
        """Serialize the request model to a Python dict.

        :return: A dict holding the request model data
        """
        d = {"ethAddress": self.eth_address, "password": self.password}
        self.validate(d)
        return d
