import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema

AUTH_LOGIN_KEYS = ("ethAddress", "password")


class AuthLoginRequest(BaseRequest):
    """

    """
    with open(resolve_schema(__file__, "auth-login.json")) as sf:
        schema = json.load(sf)

    def __init__(self, eth_address: str, password: str):
        self.eth_address = eth_address
        self.password = password

    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/auth/login"

    @property
    def method(self):
        """

        :return:
        """
        return "POST"

    @property
    def parameters(self):
        """

        :return:
        """
        return {}

    @property
    def headers(self):
        """

        :return:
        """
        return {}

    @property
    def payload(self):
        """

        :return:
        """
        return self.to_dict()

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        """

        :param d:
        :return:
        """
        cls.validate(d)
        return cls(eth_address=d["ethAddress"], password=d["password"])

    def to_dict(self):
        """

        :return:
        """
        d = {"ethAddress": self.eth_address, "password": self.password}
        self.validate(d)
        return d
