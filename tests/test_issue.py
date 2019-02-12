import json

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
VALID_ISSUE = json.dumps(
    {
        "swcID": SWC_ID,
        "swcTitle": SWC_TITLE,
        "description": {"head": DESCRIPTION_HEAD, "tail": DESCRIPTION_TAIL},
        "severity": SEVERITY,
        "locations": [
            {
                "sourceMap": SOURCE_MAP,
                "sourceType": SOURCE_TYPE,
                "sourceFormat": SOURCE_FORMAT,
                "sourceList": [SOURCE_LIST],
            }
        ],
        "extra": {},
    }
)


def test_issue_from_valid_json():
    issue = Issue.from_json(VALID_ISSUE)
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
    assert json.loads(issue) == json.loads(VALID_ISSUE)
