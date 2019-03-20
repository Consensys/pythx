from typing import Dict

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.base import BaseResponse

VERSION_KEYS = ("api", "harvey", "mythril", "maestro", "maru", "hash")


class VersionResponse(BaseResponse):
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
            maestro_version=d["maestro"],
            harvey_version=d["harvey"],
            hashed_version=d["hash"],
        )

    def to_dict(self):
        return {
            "api": self.api_version,
            "maru": self.maru_version,
            "mythril": self.mythril_version,
            "maestro": self.maestro_version,
            "harvey": self.harvey_version,
            "hash": self.hashed_version,
        }
