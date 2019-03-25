import json
from typing import Any, Dict, List

from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType
from pythx.models.util import resolve_schema


class DetectedIssuesResponse(BaseResponse):
    """The API response domain model for a report of the detected issues."""

    with open(resolve_schema(__file__, "detected-issues.json")) as sf:
        schema = json.load(sf)

    def __init__(
        self,
        issues: List[Issue],
        source_type: SourceType,
        source_format: SourceFormat,
        source_list: List[str],
        meta_data: Dict[str, Any],
    ):
        self.issues = issues
        self.source_type = source_type
        self.source_format = source_format
        self.source_list = source_list
        self.meta_data = meta_data

    @classmethod
    def from_dict(cls, d):
        """Create the response domain model from a dict.

        This also validates the dict's schema and raises a :code:`ResponseValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        d = d[0]
        return cls(
            issues=[Issue.from_dict(i) for i in d["issues"]],
            source_type=SourceType(d["sourceType"]),
            source_format=SourceFormat(d["sourceFormat"]),
            source_list=d["sourceList"],
            meta_data=d["meta"],
        )

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
        d = [
            {
                "issues": [i.to_dict() for i in self.issues],
                "sourceType": self.source_type,
                "sourceFormat": self.source_format,
                "sourceList": self.source_list,
                "meta": self.meta_data,
            }
        ]
        self.validate(d)
        return d

    def __contains__(self, key: str):
        if not type(key) == str:
            raise ValueError(
                "Expected SWC ID of type str but got {} of type {}".format(
                    key, type(key)
                )
            )
        return any(map(lambda i: i.swc_id == key, self.issues))

    def __len__(self):
        return len(self.issues)

    def __iter__(self):
        for issue in self.issues:
            yield issue

    def __getitem__(self, key):
        return self.issues[key]

    def __setitem__(self, key, value):
        self.issues[key] = value

    def __delitem__(self, key):
        del self.issues[key]
