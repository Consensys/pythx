import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.analysis import Analysis
from pythx.models.response.issue import Issue, SourceFormat, SourceType

AUTH_LOGIN_KEYS = ("access", "refresh")


class AuthRefreshResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"access": self.access_token, "refresh": self.refresh_token}
