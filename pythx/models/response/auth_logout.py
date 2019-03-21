from typing import Dict

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response.base import BaseResponse


class AuthLogoutResponse(BaseResponse):
    @classmethod
    def from_dict(cls, d: Dict):
        if not d == {}:
            raise ResponseValidationError(
                "The logout response should be empty but got data: {}".format(d)
            )
        return cls()

    def to_dict(self):
        d = {}
        return d
