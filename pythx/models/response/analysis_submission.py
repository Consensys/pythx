from pythx.models.response.analysis import Analysis
import json

from pythx.models.response.base import BaseResponse
from pythx.models.util import resolve_schema


class AnalysisSubmissionResponse(BaseResponse):
    """The API response domain model for a successful analysis job submision."""

    with open(resolve_schema(__file__, "analysis-submission.json")) as sf:
        schema = json.load(sf)

    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    @classmethod
    def from_dict(cls, d):
        """Create the response domain model from a dict.

        This also validates the dict's schema and raises a :code:`ResponseValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        return cls(analysis=Analysis.from_dict(d))

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
        d = self.analysis.to_dict()
        self.validate(d)
        return d

    def __getattr__(self, name):
        return getattr(self.analysis, name)
