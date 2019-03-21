from typing import Dict

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request.base import BaseRequest

AUTH_LOGIN_KEYS = ("ethAddress", "password")


class AuthLoginRequest(BaseRequest):
    def __init__(self, eth_address: str, password: str):
        self.eth_address = eth_address
        self.password = password

    @property
    def endpoint(self):
        return "v1/auth/login"

    @property
    def method(self):
        return "POST"

    @property
    def parameters(self):
        return {}

    @property
    def headers(self):
        return {}

    @property
    def payload(self):
        return self.to_dict()

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(eth_address=d["ethAddress"], password=d["password"])

    def to_dict(self):
        return {"ethAddress": self.eth_address, "password": self.password}
