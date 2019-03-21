from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse


class AnalysisSubmissionResponse(BaseResponse):
    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    def validate(self) -> bool:
        # return self.analysis.validate()
        pass

    @classmethod
    def from_dict(cls, d):
        return cls(analysis=Analysis.from_dict(d))

    def to_dict(self):
        return self.analysis.to_dict()
