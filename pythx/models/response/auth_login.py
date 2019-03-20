import json
from typing import Any, Dict, List

from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.util import resolve_schema

class AuthLoginResponse(BaseResponse):
    with open(resolve_schema(__file__, "auth-login.json")) as sf:
            schema = json.load(sf)

    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, d: Dict):
        cls.validate(d)
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_dict(self):
        d = {"access": self.access_token, "refresh": self.refresh_token}
        self.validate(d)
        return d
