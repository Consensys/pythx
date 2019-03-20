import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields, resolve_schema


class AuthLoginRequest(BaseRequest):
    with open(resolve_schema(__file__, "auth-login.json")) as sf:
        schema = json.load(sf)

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

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        cls.validate(d)
        return cls(eth_address=d["ethAddress"], password=d["password"])

    def to_dict(self):
        d = {"ethAddress": self.eth_address, "password": self.password}
        self.validate(d)
        return d
