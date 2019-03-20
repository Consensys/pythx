import json

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import (
    Issue,
    Severity,
    SourceFormat,
    SourceLocation,
    SourceType,
)

from . import common as testdata


def assert_issue(issue: Issue):
    assert issue.swc_id == testdata.SWC_ID
    assert issue.swc_title == testdata.SWC_TITLE
    assert issue.description_short == testdata.DESCRIPTION_HEAD
    assert issue.description_long == testdata.DESCRIPTION_TAIL
    assert issue.severity == Severity(testdata.SEVERITY)
    assert len(issue.locations) == 1
    location = issue.locations[0]
    assert location.source_map == testdata.SOURCE_MAP
    assert location.source_format == SourceFormat.EVM_BYZANTIUM_BYTECODE
    assert location.source_type == SourceType.RAW_BYTECODE
    assert location.source_list == testdata.SOURCE_LIST


def test_issue_from_valid_json():
    issue = Issue.from_json(json.dumps(testdata.ISSUE_DICT))
    assert_issue(issue)


def test_issue_from_dict():
    issue = Issue.from_dict(testdata.ISSUE_DICT)
    assert_issue(issue)


def test_issue_to_json():
    assert json.loads(testdata.ISSUE_OBJECT.to_json()) == testdata.ISSUE_DICT


def test_issue_to_dict():
    assert testdata.ISSUE_OBJECT.to_dict() == testdata.ISSUE_DICT


def test_source_location_from_dict():
    sl = SourceLocation.from_dict(testdata.SOURCE_LOCATION)
    assert sl.source_format == testdata.SOURCE_FORMAT
    assert sl.source_list == testdata.SOURCE_LIST
    assert sl.source_map == testdata.SOURCE_MAP
    assert sl.source_type == testdata.SOURCE_TYPE
