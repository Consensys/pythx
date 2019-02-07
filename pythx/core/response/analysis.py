import json
from enum import Enum

import dateutil.parser
from inflection import underscore

from pythx.core.exceptions import ResponseDecodeError
from pythx.core.util import deserialize_api_timestamp, serialize_api_timestamp

ANALYSIS_KEYS = (
    "uuid",
    "apiVersion",
    "mythrilVersion",
    "maruVersion",
    "queueTime",
    "status",
    "submittedBy",
    "submittedAt",
)


class AnalysisStatus(str, Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    ERROR = "Error"
    FINISHED = "Finished"


class Analysis:
    def __init__(
        self,
        uuid: str,
        api_version: str,
        mythril_version: str,
        maru_version: str,
        queue_time: int,
        status: AnalysisStatus,
        submitted_at: str,
        submitted_by: str,
        run_time: int = 0,
    ):
        self.uuid = uuid
        self.api_version = api_version
        self.mythril_version = mythril_version
        self.maru_version = maru_version
        self.queue_time = queue_time
        self.run_time = run_time
        self.status = AnalysisStatus[status.upper()]
        self.submitted_at = deserialize_api_timestamp(submitted_at)
        self.submitted_by = submitted_by

    @classmethod
    def from_json(cls, json_data: str):
        parsed = json.loads(json_data)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        if all(k in d for k in ANALYSIS_KEYS):
            d = {underscore(k): v for k, v in d.items()}
            return cls(**d)
        raise ResponseDecodeError(
            "Not all required keys {} found in data {}".format(ANALYSIS_KEYS, d)
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "apiVersion": self.api_version,
            "mythrilVersion": self.mythril_version,
            "maruVersion": self.maru_version,
            "queueTime": self.queue_time,
            "runTime": self.run_time,
            "status": self.status.title(),
            "submittedAt": serialize_api_timestamp(self.submitted_at),
            "submittedBy": self.submitted_by,
        }
