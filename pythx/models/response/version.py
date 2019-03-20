import json
from os import path
from typing import Any, Dict, List

import jsonschema

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.util import resolve_schema


class VersionResponse(BaseResponse):
    with open(resolve_schema(__file__, "version.json")) as sf:
        schema = json.load(sf)

    def __init__(
        self,
        api_version: str,
        maru_version: str,
        mythril_version: str,
        maestro_version: str,
        harvey_version: str,
        hashed_version: str,
    ):
        self.api_version = api_version
        self.maru_version = maru_version
        self.mythril_version = mythril_version
        self.maestro_version = maestro_version
        self.harvey_version = harvey_version
        self.hashed_version = hashed_version

    @classmethod
    def from_dict(cls, d: Dict):
        cls.validate(d)
        return cls(
            api_version=d["api"],
            maru_version=d["maru"],
            mythril_version=d["mythril"],
            maestro_version=d["maestro"],
            harvey_version=d["harvey"],
            hashed_version=d["hash"],
        )

    def to_dict(self):
        d = {
            "api": self.api_version,
            "maru": self.maru_version,
            "mythril": self.mythril_version,
            "maestro": self.maestro_version,
            "harvey": self.harvey_version,
            "hash": self.hashed_version,
        }
        self.validate(d)
        return d
