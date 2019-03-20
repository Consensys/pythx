from typing import Dict

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.base import BaseResponse


class AuthLogoutResponse(BaseResponse):
    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d: Dict):
        if not d == {}:
            raise ResponseDecodeError(
                "The logout response should be empty but got data: {}".format(d)
            )
        return cls()

    def to_dict(self):
        return {}
