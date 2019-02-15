import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError, ResponseValidationError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType

ANALYSIS_LIST_KEYS = ["analyses", "total"]


class AnalysisListResponse(BaseResponse):
    def __init__(self, analyses: List[Analysis], total: int) -> None:
        self.analyses = analyses
        self.total = total

    def validate(self) -> bool:
        if self.total < 0:
            raise ResponseValidationError(
                "Encountered invalid total value: {}".format(self.total)
            )
        # TODO: Add validation method to Analysis and call recursively

    @classmethod
    def from_dict(cls, d: dict):
        if not all(k in d for k in ANALYSIS_LIST_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(
                    ANALYSIS_LIST_KEYS, d
                )
            )
        analyses = [Analysis.from_dict(a) for a in d["analyses"]]
        return cls(analyses=analyses, total=d["total"])

    def to_dict(self):
        return {
            "analyses": [a.to_dict() for a in self.analyses],
            "total": len(self.analyses),
        }
