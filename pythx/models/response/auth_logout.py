import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.util import resolve_schema


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
