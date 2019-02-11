import json
from typing import Any, Dict, List

from pythx.core.exceptions import ResponseDecodeError
from pythx.core.response.analysis import Analysis
from pythx.core.response.issue import Issue, SourceFormat, SourceType

DETECTED_ISSUES_KEYS = ("issues", "sourceType", "sourceFormat", "sourceList", "meta")
AUTH_LOGIN_KEYS = ("access", "refresh")


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
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

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

    def to_json(self):
        return json.dumps(self.to_dict())

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


class AuthLoginResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"access": self.access_token, "refresh": self.refresh_token}


class AuthRefreshResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"access": self.access_token, "refresh": self.refresh_token}


class AuthLogoutResponse:
    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not d == {}:
            raise ResponseDecodeError(
                "The logout response should be empty but got data: {}".format(d)
            )
        return cls()

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {}
