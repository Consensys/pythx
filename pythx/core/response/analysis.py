import json
from enum import Enum

import dateutil.parser
from inflection import underscore

from pythx.core.exceptions import ResponseDecodeError

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
        self.submitted_at = dateutil.parser.parse(submitted_at)
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
            "api_version": self.api_version,
            "mythril_version": self.mythril_version,
            "maru_version": self.maru_version,
            "queue_time": self.queue_time,
            "run_time": self.run_time,
            "status": self.status,
            "submitted_at": self.submitted_at.isoformat(),
            "submitted_by": self.submitted_by,
        }
