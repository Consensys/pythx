import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields

AUTH_REFRESH_KEYS = ("access", "refresh")


class AuthRefreshRequest(BaseRequest):
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    def endpoint(self):
        return "v1/auth/refresh"

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
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in AUTH_REFRESH_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_REFRESH_KEYS, d)
            )
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"access": self.access_token, "refresh": self.refresh_token}
