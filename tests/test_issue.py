import json
import pytest
from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import (
    Issue,
    Severity,
    SourceFormat,
    SourceLocation,
    SourceType,
)

SWC_ID = "SWC-103"
SWC_TITLE = "Floating Pragma"
DESCRIPTION_HEAD = "A floating pragma is set."
DESCRIPTION_TAIL = 'It is recommended to make a conscious choice on what version of Solidity is used for compilation. Currently any version equal or greater than \\"0.4.24\\" is allowed.'
SEVERITY = "Low"
SOURCE_MAP = "48:1:0"
SOURCE_TYPE = "raw-bytecode"
SOURCE_FORMAT = "evm-byzantium-bytecode"
SOURCE_LIST = "/test/my-super-safe-contract.sol"
SOURCE_LOCATION = {
                "sourceMap": SOURCE_MAP,
                "sourceType": SOURCE_TYPE,
                "sourceFormat": SOURCE_FORMAT,
                "sourceList": [SOURCE_LIST],
            }
VALID_ISSUE = {
        "swcID": SWC_ID,
        "swcTitle": SWC_TITLE,
        "description": {"head": DESCRIPTION_HEAD, "tail": DESCRIPTION_TAIL},
        "severity": SEVERITY,
        "locations": [
            SOURCE_LOCATION
        ],
        "extra": {},
    }


def assert_issue(issue: Issue):
    assert issue.swc_id == SWC_ID
    assert issue.swc_title == SWC_TITLE
    assert issue.description_short == DESCRIPTION_HEAD
    assert issue.description_long == DESCRIPTION_TAIL
    assert issue.severity == Severity.LOW
    assert len(issue.locations) == 1
    location = issue.locations[0]
    assert location.source_map == SOURCE_MAP
    assert location.source_format == SourceFormat.EVM_BYZANTIUM_BYTECODE
    assert location.source_type == SourceType.RAW_BYTECODE
    assert location.source_list == [SOURCE_LIST]


def test_issue_from_valid_json():
    issue = Issue.from_json(json.dumps(VALID_ISSUE))
    assert_issue(issue)


def test_issue_from_dict():
    issue = Issue.from_dict(VALID_ISSUE)
    assert_issue(issue)


def test_issue_to_json():
    issue = Issue(
        swc_id=SWC_ID,
        swc_title=SWC_TITLE,
        description_short=DESCRIPTION_HEAD,
        description_long=DESCRIPTION_TAIL,
        severity=Severity.LOW,
        locations=[
            SourceLocation(
                source_map=SOURCE_MAP,
                source_type=SourceType.RAW_BYTECODE,
                source_format=SourceFormat.EVM_BYZANTIUM_BYTECODE,
                source_list=[SOURCE_LIST],
            )
        ],
        extra={},
    ).to_json()
    assert json.loads(issue) == VALID_ISSUE


def test_issue_to_dict():
    issue = Issue(
        swc_id=SWC_ID,
        swc_title=SWC_TITLE,
        description_short=DESCRIPTION_HEAD,
        description_long=DESCRIPTION_TAIL,
        severity=Severity.LOW,
        locations=[
            SourceLocation(
                source_map=SOURCE_MAP,
                source_type=SourceType.RAW_BYTECODE,
                source_format=SourceFormat.EVM_BYZANTIUM_BYTECODE,
                source_list=[SOURCE_LIST],
            )
        ],
        extra={},
    ).to_dict()
    assert issue == VALID_ISSUE


def test_source_location_from_dict():
    sl = SourceLocation.from_dict(SOURCE_LOCATION)
    assert sl.source_format == SOURCE_FORMAT
    assert sl.source_list == [SOURCE_LIST]
    assert sl.source_map == SOURCE_MAP
    assert sl.source_type == SOURCE_TYPE


def test_source_location_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        SourceLocation.from_dict({})


def test_source_location_validate():
    SourceLocation.from_dict(SOURCE_LOCATION).validate()
