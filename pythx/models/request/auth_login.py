import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.util import dict_delete_none_fields

AUTH_LOGIN_KEYS = ("ethAddress", "password", "userId")


class AuthLoginRequest:
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

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(
            eth_address=d["ethAddress"], password=d["password"], user_id=d["userId"]
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "ethAddress": self.eth_address,
            "password": self.password,
            "userId": self.user_id,
        }
