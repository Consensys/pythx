import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields

ANALYSIS_SUBMISSION_KEYS = ("bytecode", "sources")


class AnalysisSubmissionRequest(BaseRequest):
    def __init__(
        self,
        contract_name: str = None,
        bytecode: str = None,
        source_map: str = None,
        deployed_bytecode: str = None,
        deployed_source_map: str = None,
        sources: Dict[str, Dict[str, str]] = None,
        source_list: List[str] = None,
        solc_version: str = None,
        analysis_mode: str = "quick",
    ):
        self.contract_name = contract_name
        self.bytecode = bytecode
        self.source_map = source_map
        self.deployed_bytecode = deployed_bytecode
        self.deployed_source_map = deployed_source_map
        self.sources = sources
        self.source_list = source_list
        self.solc_version = solc_version
        self.analysis_mode = analysis_mode

    @property
    def endpoint(self):
        return "v1/analyses"

    @property
    def method(self):
        return "POST"

    @property
    def parameters(self):
        return {}

    @property
    def headers(self):
        return {}

    @property
    def payload(self):
        return {"data": self.to_dict()}

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
        base_dict = {
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

        return dict_delete_none_fields(base_dict)
