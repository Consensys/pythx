from typing import List, Dict, Any
import json
from pythx.core.exceptions import ResponseDecodeError
from pythx.core.response.analysis import Analysis
from pythx.core.response.issue import Issue, SourceType, SourceFormat


DETECTED_ISSUES_KEYS = (
    "uuid",
    "issues",
    "sourceType",
    "sourceFormat",
    "sourceList",
    "meta",
)


class AnalysisListResponse:
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
        analyses = []
        for analysis in d:
            analyses.append(Analysis.from_dict(analysis))
        return cls(analyses=analyses)  # TODO: Add total

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return [a.to_dict() for a in self.analyses]


class AnalysisSubmissionResponse:
    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    def validate(self) -> bool:
        # return self.analysis.validate()
        pass

    @classmethod
    def from_json(cls, json_str: str):
        analysis = json.loads(json_str)
        return cls.from_dict(analysis)

    @classmethod
    def from_dict(cls, d):
        return cls(analysis=Analysis.from_dict(d))

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.analysis.to_dict()


# Same properties as submission response
class AnalysisStatusResponse(AnalysisSubmissionResponse):
    pass


class DetectedIssuesResponse:
    def __init__(
        self,
        uuid: str,
        issues: List[Issue],
        source_type: SourceType,
        source_format: SourceFormat,
        source_list: List[str],
        meta_data: Dict[str, Any],
    ):
        self.uuid = uuid
        self.issues = issues
        self.source_type = source_type
        self.source_format = source_format
        self.source_list = source_list
        self.meta_data = meta_data

    def validate(self) -> bool:
        pass

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        if not all(k in d for k in DETECTED_ISSUES_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(
                    DETECTED_ISSUES_KEYS, d
                )
            )
        return cls(
            uuid=d["uuid"],
            issues=[Issue.from_dict(i) for i in d["issues"]],
            source_type=SourceType[d["sourceType"].upper()],
            source_format=SourceFormat[d["sourceFormat"].upper()],
            source_list=d["sourceList"],
            meta_data=d["meta"],
        )

    def to_json(self):
        json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "issues": [i.to_dict() for i in self.issues],
            "sourceType": self.source_type,
            "sourceFormat": self.source_format,
            "sourceList": self.source_list,
            "meta": self.meta_data
        }
