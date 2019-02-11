import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.core.exceptions import RequestDecodeError, RequestValidationError
from pythx.core.util import dict_delete_none_fields

ANALYSIS_LIST_KEYS = ("offset", "dateFrom", "dateTo")
ANALYSIS_SUBMISSION_KEYS = ("bytecode", "sources")
AUTH_LOGIN_KEYS = ("ethAddress", "password", "userId")
AUTH_REFRESH_KEYS = ("access", "refresh")


class AnalysisListRequest:
    def __init__(self, offset: int, date_from: datetime, date_to: datetime):
        self.offset = offset
        self.date_from = date_from
        self.date_to = date_to

    @property
    @staticmethod
    def endpoint():
        return "/analyses"

    @property
    @staticmethod
    def method():
        return "GET"

    def payload(self):
        return self.to_dict()

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
    @staticmethod
    def endpoint():
        return "/analyses"

    @property
    @staticmethod
    def method():
        return "POST"

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


class AnalysisStatusRequest:
    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    @staticmethod
    def method():
        return "GET"

    @property
    def endpoint(self):
        return "/analyses/{}".format(self.uuid)

    def payload(self):
        return {}

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        uuid = d.get("uuid")
        if uuid is None:
            raise RequestDecodeError("Missing uuid field in data {}".format(d))
        return cls(uuid=uuid)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"uuid": self.uuid}


class DetectedIssuesRequest(AnalysisStatusRequest):
    def __init__(self, uuid: str):
        super().__init__(uuid)

    @property
    def endpoint(self):
        return "/analyses/{}/issues".format(self.uuid)

    @property
    @staticmethod
    def method():
        return "GET"


class AuthLoginRequest:
    def __init__(self, eth_address: str, password: str, user_id: str):
        self.eth_address = eth_address
        self.password = password
        self.user_id = user_id

    @property
    @staticmethod
    def endpoint():
        return "/auth/login"

    @property
    @staticmethod
    def method():
        return "POST"

    def payload(self):
        return self.to_dict()

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        if not all(k in d for k in AUTH_LOGIN_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_LOGIN_KEYS, d)
            )
        return cls(
            eth_address=d["ethAddress"], password=d["password"], user_id=d["userId"]
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "ethAddress": self.eth_address,
            "password": self.password,
            "userId": self.user_id,
        }


class AuthRefreshRequest:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    @staticmethod
    def endpoint():
        return "/auth/refresh"

    @property
    @staticmethod
    def method():
        return "POST"

    def payload(self):
        return self.to_dict()

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if not all(k in d for k in AUTH_REFRESH_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(AUTH_REFRESH_KEYS, d)
            )
        return cls(access_token=d["access"], refresh_token=d["refresh"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"access": self.access_token, "refresh": self.refresh_token}


class AuthLogoutRequest:
    def __init__(self, global_: bool):
        self.global_ = global_

    @property
    @staticmethod
    def endpoint():
        return "/auth/logout"

    @property
    @staticmethod
    def method():
        return "POST"

    def payload(self):
        return {}

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d: Dict):
        if "global" not in d:
            raise RequestDecodeError("Required key 'global' not in data {}".format(d))
        return cls(global_=d["global"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"global": self.global_}
