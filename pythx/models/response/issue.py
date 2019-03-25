"""This module contains domain models regrading found issues."""

import json
from enum import Enum
from typing import Any, Dict, List


class Severity(str, Enum):
    """An Enum holding the possible severities an issue can have."""

    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class SourceType(str, Enum):
    """An Enum holding the possible source type values."""

    RAW_BYTECODE = "raw-bytecode"
    ETHEREUM_ADDRESS = "ethereum-address"
    SOLIDITY_CONTRACT = "solidity-contract"
    SOLIDITY_FILE = "solidity-file"


class SourceFormat(str, Enum):
    """An Enum holding the possible source format values."""

    TEXT = "text"
    SOLC_AST_LEGACY_JSON = "solc-ast-legacy-json"
    SOLC_AST_COMPACT_JSON = "solc-ast-compact-json"
    EVM_BYZANTIUM_BYTECODE = "evm-byzantium-bytecode"
    EWASM_RAW = "ewasm-raw"


class SourceLocation:
    """The domain model for a source location in a detected issue."""

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
        """Create the response domain model from a dict.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        return cls(
            source_map=d["sourceMap"],
            source_type=SourceType(d["sourceType"]),
            source_format=SourceFormat(d["sourceFormat"]),
            source_list=d["sourceList"],
        )

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
        return {
            "sourceMap": self.source_map,
            "sourceType": self.source_type,
            "sourceFormat": self.source_format,
            "sourceList": self.source_list,
        }


class Issue:
    """The API response domain model for a single issue object."""

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
        """

        :param json_data:
        :return:
        """
        parsed = json.loads(json_data)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        """Create the response domain model from a dict.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
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
        """Serialize the model to JSON format.

        Internally, this method is using the :code:`to_dict` method.

        :return: A JSON string holding the model's data
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
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
