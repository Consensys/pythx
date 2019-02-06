from enum import Enum
from typing import List, Dict, Any, Tuple
import json
from inflection import underscore
from pythx.core.exceptions import ResponseDecodeError


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

    @classmethod
    def from_dict(cls, d):
        source_map = d.get("sourceMap")
        source_type = d.get("sourceType")
        if source_type is None:
            raise ResponseDecodeError(
                "sourceType field not found in location object: {}".format(d)
            )
        else:
            # to resolve into enum value
            source_type = source_type.replace("-", "_").upper()
        source_format = d.get("sourceFormat")
        if source_format is None:
            raise ResponseDecodeError(
                "sourceFormat field not found in location object: {}".format(d)
            )
        else:
            # to resolve into enum value
            source_format = source_format.replace("-", "_").upper()
        source_list = d.get("sourceList")
        return cls(
            source_map=source_map,
            source_type=SourceType[source_type],
            source_format=SourceFormat[source_format],
            source_list=source_list,
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
        self.severity = Severity[severity.upper()]
        self.locations = locations
        self.extra_data = extra

    @classmethod
    def from_json(cls, json_data: str):
        parsed = json.loads(json_data)
        parsed = {underscore(k): v for k, v in parsed.items()}
        parsed["description_short"] = parsed["description"]["head"]
        parsed["description_long"] = parsed["description"]["tail"]
        del parsed["description"]
        locs = []
        for loc in parsed["locations"]:
            locs.append(
                SourceLocation(
                    source_map=loc["sourceMap"],
                    source_type=loc["sourceType"],
                    source_format=loc["sourceFormat"],
                    source_list=loc["sourceList"],
                )
            )
        parsed["locations"] = locs
        return cls(**parsed)

    def to_json(self):
        return json.dumps(
            {
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
        )
