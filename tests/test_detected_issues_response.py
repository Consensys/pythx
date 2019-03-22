import json
from copy import deepcopy

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import (
    DetectedIssuesResponse,
    Issue,
    Severity,
    SourceFormat,
    SourceLocation,
    SourceType,
)

from . import common as testdata


def assert_detected_issues(resp):
    assert len(resp.issues) == 1
    issue = resp.issues[0]
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


def test_detected_issues_from_valid_json():
    resp = DetectedIssuesResponse.from_json(
        json.dumps(testdata.DETECTED_ISSUES_RESPONSE_DICT)
    )
    assert_detected_issues(resp)


def test_detected_issues_from_invalid_json():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_json("[]")


def test_detected_issues_from_dict():
    resp = DetectedIssuesResponse.from_dict(testdata.DETECTED_ISSUES_RESPONSE_DICT)
    assert_detected_issues(resp)


def test_detected_issues_from_invalid_list():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_dict([])


def test_detected_issues_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_dict({})


def test_detected_issues_to_json():
    json_str = testdata.DETECTED_ISSUES_RESPONSE_OBJECT.to_json()
    assert json.loads(json_str) == testdata.DETECTED_ISSUES_RESPONSE_DICT


def test_detected_issues_to_dict():
    resp = testdata.DETECTED_ISSUES_RESPONSE_OBJECT.to_dict()
    assert testdata.DETECTED_ISSUES_RESPONSE_DICT == resp


def test_valid_swc_id_contains():
    assert testdata.SWC_ID in testdata.DETECTED_ISSUES_RESPONSE_OBJECT


def test_valid_swc_id_not_contains():
    assert not "SWC-104" in testdata.DETECTED_ISSUES_RESPONSE_OBJECT


def test_invalid_key_contains():
    with pytest.raises(ValueError):
        1337 in testdata.DETECTED_ISSUES_RESPONSE_OBJECT


def test_response_length():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    assert len(resp) == len(resp.issues)
    resp.issues.append("foo")
    assert len(resp) == len(resp.issues)


def test_issue_iterator():
    for i, issue in enumerate(testdata.DETECTED_ISSUES_RESPONSE_OBJECT):
        assert testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issues[i] == issue


def test_issue_valid_getitem():
    assert (
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT[0]
        == testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issues[0]
    )


def test_invalid_getitem():
    with pytest.raises(IndexError):
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT[1337]


def test_valid_setitem():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    resp[0] = "foo"
    assert resp[0] == "foo"
    assert resp.issues[0] == "foo"


def test_invalid_setitem():
    with pytest.raises(TypeError):
        # string key on list access
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT["foo"]


def test_valid_delete():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    del resp[0]
    assert resp.issues == []


def test_invalid_delete():
    with pytest.raises(IndexError):
        del testdata.DETECTED_ISSUES_RESPONSE_OBJECT[1337]
