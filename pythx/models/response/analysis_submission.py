from pythx.models.response.analysis import Analysis
import json

from pythx.models.response.base import BaseResponse
from pythx.models.util import resolve_schema


class AnalysisSubmissionResponse(BaseResponse):
    """

    """
    with open(resolve_schema(__file__, "analysis-submission.json")) as sf:
        schema = json.load(sf)

    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    @classmethod
    def from_dict(cls, d):
        """

        :param d:
        :return:
        """
        cls.validate(d)
        return cls(analysis=Analysis.from_dict(d))

    def to_dict(self):
        """

        :return:
        """
        d = self.analysis.to_dict()
        self.validate(d)
        return d

    def __getattr__(self, name):
        return getattr(self.analysis, name)
