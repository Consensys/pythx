from enum import Enum

from inflection import underscore

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.base import BaseResponse
from pythx.models.util import deserialize_api_timestamp, serialize_api_timestamp

ANALYSIS_KEYS = (
    "uuid",
    "apiVersion",
    "mythrilVersion",
    "maestroVersion",
    "harveyVersion",
    "maruVersion",
    "queueTime",
    "status",
    "submittedBy",
    "submittedAt",
)


class AnalysisStatus(str, Enum):
    QUEUED = "Queued"
    IN_PROGRESS = "In Progress"
    ERROR = "Error"
    FINISHED = "Finished"


class Analysis(BaseResponse):
    def __init__(
        self,
        uuid: str,
        api_version: str,
        mythril_version: str,
        maestro_version: str,
        harvey_version: str,
        maru_version: str,
        queue_time: int,
        status: AnalysisStatus,
        submitted_at: str,
        submitted_by: str,
        run_time: int = 0,
        error: str = None,
    ):
        self.uuid = uuid
        self.api_version = api_version
        self.mythril_version = mythril_version
        self.maestro_version = maestro_version
        self.harvey_version = harvey_version
        self.maru_version = maru_version
        self.queue_time = queue_time
        self.run_time = run_time
        self.status = AnalysisStatus(status.title())
        self.submitted_at = deserialize_api_timestamp(submitted_at)
        self.submitted_by = submitted_by
        self.error = error

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d):
        if all(k in d for k in ANALYSIS_KEYS):
            d = {underscore(k): v for k, v in d.items()}
            return cls(**d)
        raise ResponseDecodeError(
            "Not all required keys {} found in data {}".format(ANALYSIS_KEYS, d)
        )

    def to_dict(self):
        d = {
            "uuid": self.uuid,
            "apiVersion": self.api_version,
            "mythrilVersion": self.mythril_version,
            "maestroVersion": self.maestro_version,
            "harveyVersion": self.harvey_version,
            "maruVersion": self.maru_version,
            "queueTime": self.queue_time,
            "runTime": self.run_time,
            "status": self.status.title(),
            "submittedAt": serialize_api_timestamp(self.submitted_at),
            "submittedBy": self.submitted_by,
        }
        if self.error is not None:
            d.update({"error": self.error})

        return d
