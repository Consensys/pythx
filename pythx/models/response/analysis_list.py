import json
from typing import List

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.util import resolve_schema

INDEX_ERROR_MSG = "Analysis at index {} was not fetched"


class AnalysisListResponse(BaseResponse):
    with open(resolve_schema(__file__, "analysis-list.json")) as sf:
        schema = json.load(sf)

    def __init__(self, analyses: List[Analysis], total: int) -> None:
        self.analyses = analyses
        self.total = total

    @classmethod
    def validate(cls, candidate):
        super().validate(candidate)
        if not type(candidate) == dict:
            raise ResponseValidationError(
                "Expected type dict but got {}".format(type(candidate))
            )

    @classmethod
    def from_dict(cls, d: dict):
        cls.validate(d)
        analyses = [Analysis.from_dict(a) for a in d["analyses"]]
        return cls(analyses=analyses, total=d["total"])

    def to_dict(self):
        d = {
            "analyses": [a.to_dict() for a in self.analyses],
            "total": len(self.analyses),
        }
        self.validate(d)
        return d

    def __iter__(self):
        for analysis in self.analyses:
            yield analysis

    def __getitem__(self, idx):
        try:
            return self.analyses[idx]
        except IndexError:
            raise IndexError(INDEX_ERROR_MSG.format(idx))

    def __setitem__(self, idx, value):
        try:
            self.analyses[idx] = value
        except IndexError:
            raise IndexError(INDEX_ERROR_MSG.format(idx))

    def __delitem__(self, idx):
        try:
            del self.analyses[idx]
            self.total -= 1
        except IndexError:
            raise IndexError(INDEX_ERROR_MSG.format(idx))

    def __len__(self):
        return self.total

    def __reversed__(self):
        return reversed(self.analyses)

    def __contains__(self, item):
        if not type(item) in (Analysis, str):
            raise ValueError(
                "Expected type Analysis or str but got {}".format(type(item))
            )
        uuid = item.uuid if type(item) == Analysis else item
        return uuid in map(lambda x: x.uuid, self.analyses)

    def __eq__(self, candidate):
        return self.total == candidate.total and self.analyses == candidate.analyses
