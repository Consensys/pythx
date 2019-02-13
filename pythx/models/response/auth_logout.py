import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType


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
