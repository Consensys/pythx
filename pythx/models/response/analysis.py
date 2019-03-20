import json
from enum import Enum

import dateutil.parser
from inflection import underscore

from pythx.models.response.base import BaseResponse
from pythx.models.util import deserialize_api_timestamp, serialize_api_timestamp


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

    @classmethod
    def from_dict(cls, d):
        d = {underscore(k): v for k, v in d.items()}
        return cls(**d)

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

    def __eq__(self, candidate):
        return all((
            self.uuid == candidate.uuid,
            self.api_version == candidate.api_version,
            self.mythril_version == candidate.mythril_version,
            self.maestro_version == candidate.maestro_version,
            self.harvey_version == candidate.harvey_version,
            self.maru_version == candidate.maru_version,
            self.queue_time == candidate.queue_time,
            self.run_time == candidate.run_time,
            self.status == candidate.status,
            self.submitted_at == candidate.submitted_at,
            self.submitted_by == candidate.submitted_by,
            self.error == candidate.error
        ))

    def __repr__(self):
        return "<Analysis uuid={} status={}>".format(self.uuid, self.status)
