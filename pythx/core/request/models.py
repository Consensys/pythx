from typing import Dict, Any, List
import json
from datetime import datetime
import dateutil.parser
from pythx.core.exceptions import RequestValidationError, RequestDecodeError


ANALYSIS_LIST_KEYS = ("offset", "dateFrom", "dateTo")
ANALYSIS_SUBMISSION_KEYS = ("bytecode", "sources")


class AnalysisListRequest:
    def __init__(self, offset: int, date_from: datetime, date_to: datetime):
        self.offset = offset
        self.date_from = date_from
        self.date_to = date_to

    def validate(self):
        return (self.date_from <= self.date_to) and self.offset >= 0

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        if not all(k in d for k in ANALYSIS_LIST_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(
                    ANALYSIS_LIST_KEYS, d
                )
            )
        req = cls(
            offset=d["offset"],
            date_from=dateutil.parser.parse(d["dateFrom"]),
            date_to=dateutil.parser.parse(d["dateTo"]),
        )
        if not req.validate():
            raise RequestValidationError("Request validation failed for {}".format(req))

        return req

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "offset": self.offset,
            "dateFrom": self.date_from.isoformat(),
            "dateTo": self.date_to.isoformat(),
        }


class AnalysisSubmissionRequest:
    def __init__(
        self,
        contract_name=None,
        bytecode=None,
        source_map=None,
        deployed_bytecode=None,
        deployed_source_map=None,
        sources=None,
        source_list=None,
        solc_version=None,
        analysis_mode="quick",
    ):
        self.contract_name: str = contract_name
        self.bytecode: str = bytecode
        self.source_map: str = source_map
        self.deployed_bytecode: str = deployed_bytecode
        self.deployed_source_map: str = deployed_source_map
        self.sources: Dict[str, Dict[str, str]] = sources
        self.source_list: List[str] = source_list
        self.solc_version: str = solc_version
        self.analysis_mode: str = analysis_mode

    def validate(self):
        valid = True
        msg = "Error validating analysis submission request: {}"
        if self.analysis_mode not in ("full", "quick"):
            valid = False
            msg = msg.format("Analysis mode must be one of {full,quick}")
        elif not (self.bytecode or self.sources):
            valid = False
            msg = msg.format("Must pass at least bytecode or source field")
        # TODO: MOAR

        if not valid:
            raise RequestValidationError(msg)

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if type(d) is not dict or not any(k in d for k in ANALYSIS_SUBMISSION_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(
                    ANALYSIS_SUBMISSION_KEYS, d
                )
            )

        # TODO: Should we validate here?
        return cls(
            contract_name=d.get("contractName"),
            bytecode=d.get("bytecode"),
            source_map=d.get("sourceMap"),
            deployed_bytecode=d.get("deployedBytecode"),
            deployed_source_map=d.get("deployedSourceMap"),
            sources=d.get("sources"),
            source_list=d.get("sourceList"),
            solc_version=d.get("version"),
            analysis_mode=d.get("analysisMode"),
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "contractName": self.contract_name,
            "bytecode": self.bytecode,
            "sourceMap": self.source_map,
            "deployedBytecode": self.deployed_bytecode,
            "deployedSourceMap": self.deployed_source_map,
            "sources": self.sources,
            "sourceList": self.source_list,
            "version": self.solc_version,
            "analysisMode": self.analysis_mode,
        }


class AnalysisStatusRequest:
    pass


class DetectedIssuesRequest:
    pass
