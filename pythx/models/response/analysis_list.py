import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.analysis import Analysis
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.response.base import BaseResponse


class AnalysisListResponse(BaseResponse):
    def __init__(self, analyses: List[Analysis], total: int = 0) -> None:
        self.analyses = analyses
        self.total = total  # TODO: Add total once format clear

    def validate(self) -> bool:
        if self.total < 0:
            return False
        # TODO: Add validation method to Analysis and call recursively

    @classmethod
    def from_json(cls, json_str: str):
        analysis_list = json.loads(json_str)
        return cls.from_dict(analysis_list)

    @classmethod
    def from_dict(cls, d: List[Dict[str, Any]]):
        if type(d) != list:
            raise ResponseDecodeError("Expected JSON list but got {}".format(d))
        analyses = []
        for analysis in d:
            analyses.append(Analysis.from_dict(analysis))
        return cls(analyses=analyses)  # TODO: Add total

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return [a.to_dict() for a in self.analyses]
