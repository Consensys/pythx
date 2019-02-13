import json
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.analysis import Analysis
from pythx.models.response.base import BaseResponse
from pythx.models.response.issue import Issue, SourceFormat, SourceType

DETECTED_ISSUES_KEYS = ("issues", "sourceType", "sourceFormat", "sourceList", "meta")


class DetectedIssuesResponse(BaseResponse):
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

    def validate(self) -> bool:
        pass

    @classmethod
    def from_dict(cls, d):
        if (
            type(d) != list
            or len(d) != 1
            or all(k not in d[0] for k in DETECTED_ISSUES_KEYS)
        ):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(
                    DETECTED_ISSUES_KEYS, d
                )
            )
        d = d[0]
        return cls(
            issues=[Issue.from_dict(i) for i in d["issues"]],
            source_type=SourceType(d["sourceType"]),
            source_format=SourceFormat(d["sourceFormat"]),
            source_list=d["sourceList"],
            meta_data=d["meta"],
        )

    def to_dict(self):
        return [
            {
                "issues": [i.to_dict() for i in self.issues],
                "sourceType": self.source_type,
                "sourceFormat": self.source_format,
                "sourceList": self.source_list,
                "meta": self.meta_data,
            }
        ]
