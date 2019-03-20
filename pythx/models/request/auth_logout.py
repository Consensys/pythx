from typing import Dict

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request.base import BaseRequest


class AuthLogoutRequest(BaseRequest):
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

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d: Dict):
        if "global" not in d:
            raise RequestDecodeError("Required key 'global' not in data {}".format(d))
        return cls(global_=d["global"])

    def to_dict(self):
        return {"global": self.global_}
