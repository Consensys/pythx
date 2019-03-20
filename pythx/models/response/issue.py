import json
from enum import Enum
from typing import Any, Dict, List

from pythx.models.exceptions import ResponseDecodeError

SOURCE_LOCATION_KEYS = ("sourceMap", "sourceType", "sourceFormat", "sourceList")


class Severity(str, Enum):
    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class SourceType(str, Enum):
    RAW_BYTECODE = "raw-bytecode"
    ETHEREUM_ADDRESS = "ethereum-address"
    SOLIDITY_CONTRACT = "solidity-contract"
    SOLIDITY_FILE = "solidity-file"


class SourceFormat(str, Enum):
    TEXT = "text"
    SOLC_AST_LEGACY_JSON = "solc-ast-legacy-json"
    SOLC_AST_COMPACT_JSON = "solc-ast-compact-json"
    EVM_BYZANTIUM_BYTECODE = "evm-byzantium-bytecode"
    EWASM_RAW = "ewasm-raw"


class SourceLocation:
    def __init__(
        self,
        source_map: str,
        source_type: SourceType,
        source_format: SourceFormat,
        source_list: List[str],
    ):
        self.source_map = source_map
        self.source_type = source_type
        self.source_format = source_format
        self.source_list = source_list

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d):
        if not all(k in d for k in SOURCE_LOCATION_KEYS):
            raise ResponseDecodeError(
                "Not all required keys {} found in data {}".format(
                    SOURCE_LOCATION_KEYS, d
                )
            )

        return cls(
            source_map=d["sourceMap"],
            source_type=SourceType(d["sourceType"]),
            source_format=SourceFormat(d["sourceFormat"]),
            source_list=d["sourceList"],
        )

    def to_dict(self):
        return {
            "sourceMap": self.source_map,
            "sourceType": self.source_type,
            "sourceFormat": self.source_format,
            "sourceList": self.source_list,
        }


class Issue:
    def __init__(
        self,
        swc_id: str,
        swc_title: str,
        description_short: str,
        description_long: str,
        severity: Severity,
        locations: List[SourceLocation],
        extra: Dict[str, Any],
    ):
        self.swc_id = swc_id
        self.swc_title = swc_title
        self.description_short = description_short
        self.description_long = description_long
        self.severity = severity
        self.locations = locations
        self.extra_data = extra

    @classmethod
    def from_json(cls, json_data: str):
        parsed = json.loads(json_data)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        # TODO: validate
        locs = [
            SourceLocation(
                source_map=loc.get("sourceMap"),
                source_type=loc.get("sourceType"),
                source_format=loc.get("sourceFormat"),
                source_list=loc.get("sourceList"),
            )
            for loc in d["locations"]
        ]
        return cls(
            swc_id=d["swcID"],
            swc_title=d["swcTitle"],
            description_short=d["description"]["head"],
            description_long=d["description"]["tail"],
            severity=Severity(d["severity"]) if d["severity"] else Severity.NONE,
            locations=locs,
            extra=d["extra"],
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "swcID": self.swc_id,
            "swcTitle": self.swc_title,
            "description": {
                "head": self.description_short,
                "tail": self.description_long,
            },
            "severity": self.severity,
            "locations": [loc.to_dict() for loc in self.locations],
            "extra": self.extra_data,
        }
