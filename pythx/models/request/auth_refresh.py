import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema


class AuthRefreshRequest(BaseRequest):
    with open(resolve_schema(__file__, "auth-refresh.json")) as sf:
        schema = json.load(sf)

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
        return {"accessToken": self.access_token, "refreshToken": self.refresh_token}

    @classmethod
    def from_dict(cls, d: Dict):
        cls.validate(d)
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_dict(self):
        d = {"access": self.access_token, "refresh": self.refresh_token}
        self.validate(d)
        return d
