import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields, resolve_schema


class AuthLogoutRequest(BaseRequest):
    with open(resolve_schema(__file__, "auth-logout.json")) as sf:
        schema = json.load(sf)

    def __init__(self, global_: bool = False):
        self.global_ = global_

    @property
    def endpoint(self):
        return "v1/auth/logout"

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
        return {}

    @classmethod
    def from_dict(cls, d: Dict):
        cls.validate(d)
        return cls(global_=d["global"])

    def to_dict(self):
        d = {"global": self.global_}
        self.validate(d)
        return d
