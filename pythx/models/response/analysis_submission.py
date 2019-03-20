import json
from typing import Any, Dict, List

from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.util import resolve_schema


class AnalysisSubmissionResponse(BaseResponse):
    with open(resolve_schema(__file__, "analysis-submission.json")) as sf:
        schema = json.load(sf)

    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    @classmethod
    def from_dict(cls, d):
        cls.validate(d)
        return cls(analysis=Analysis.from_dict(d))

    def to_dict(self):
        d = self.analysis.to_dict()
        self.validate(d)
        return d

    def __getattr__(self, name):
        return getattr(self.analysis, name)
