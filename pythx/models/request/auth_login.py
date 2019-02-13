import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields

AUTH_LOGIN_KEYS = ("ethAddress", "password", "userId")


class AuthLoginRequest(BaseRequest):
    def __init__(self, eth_address: str, password: str, user_id: str):
        self.eth_address = eth_address
        self.password = password
        self.user_id = user_id

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
        return cls(
            eth_address=d["ethAddress"], password=d["password"], user_id=d["userId"]
        )

    def to_dict(self):
        return {
            "ethAddress": self.eth_address,
            "password": self.password,
            "userId": self.user_id,
        }
