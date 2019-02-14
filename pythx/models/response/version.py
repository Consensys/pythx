import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType

VERSION_KEYS = ("api", "harvey", "mythril", "maru", "hash")


class VersionResponse(BaseResponse):
    def __init__(
        self,
        api_version: str,
        maru_version: str,
        mythril_version: str,
        harvey_version: str,
        hashed_version: str,
    ):
        self.api_version = api_version
        self.maru_version = maru_version
        self.mythril_version = mythril_version
        self.harvey_version = harvey_version
        self.hashed_version = hashed_version

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in VERSION_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(VERSION_KEYS, d)
            )
        return cls(
            api_version=d["api"],
            maru_version=d["maru"],
            mythril_version=d["mythril"],
            harvey_version=d["harvey"],
            hashed_version=d["hash"],
        )

    def to_dict(self):
        return {
            "api": self.api_version,
            "maru": self.maru_version,
            "mythril": self.mythril_version,
            "harvey": self.harvey_version,
            "hash": self.hashed_version,
        }
