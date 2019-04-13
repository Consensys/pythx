import json
from copy import deepcopy

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import (
    DetectedIssuesResponse,
    Issue,
    IssueReport,
    Severity,
    SourceFormat,
    SourceLocation,
    SourceType,
)

from . import common as testdata


def assert_detected_issues(resp):
    assert len(resp.issue_reports) == 1
    report = resp.issue_reports[0]
    assert type(report) == IssueReport
    issue = report.issues[0]
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
        # DetectedIssuesResponse,
        json.dumps(testdata.DETECTED_ISSUES_RESPONSE_DICT)
    )
    assert_detected_issues(resp)


def test_detected_issues_from_invalid_json():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_json("[]")


def test_detected_issues_from_dict():
    resp = DetectedIssuesResponse.from_dict(testdata.DETECTED_ISSUES_RESPONSE_DICT)
    assert_detected_issues(resp)


def test_detected_issues_from_list():
    resp = DetectedIssuesResponse.from_dict([testdata.ISSUE_REPORT_DICT])
    assert_detected_issues(resp)


def test_detected_issues_from_invalid_type():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_dict("foo")


def test_detected_issues_from_invalid_list():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_dict([])


def test_detected_issues_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        DetectedIssuesResponse.from_dict({})


def test_detected_issues_to_json():
    json_str = testdata.DETECTED_ISSUES_RESPONSE_OBJECT.to_json()
    assert (
        json.loads(json_str) == testdata.DETECTED_ISSUES_RESPONSE_DICT["issueReports"]
    )


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
    total_report_issues = len(resp)
    assert len(resp) == total_report_issues
    resp.issue_reports.append(
        IssueReport(
            issues=["foo", "bar"],
            source_type=SourceType.RAW_BYTECODE,
            source_format=SourceFormat.EVM_BYZANTIUM_BYTECODE,
            source_list="foo.sol",
            meta_data={},
        )
    )
    assert len(resp) == total_report_issues + 2


def test_issue_iterator():
    for i, report in enumerate(testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issue_reports):
        assert testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issue_reports[i] == report


def test_report_iterator():
    report = testdata.DETECTED_ISSUES_RESPONSE_OBJECT
    for i, issue in enumerate(report):
        assert issue == report.issue_reports[0][i]


def test_issue_valid_getitem():
    assert (
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issue_reports[0]
        == testdata.DETECTED_ISSUES_RESPONSE_OBJECT[0]
    )


def test_report_getitem():
    report = testdata.DETECTED_ISSUES_RESPONSE_OBJECT
    for i, issue in enumerate(report):
        assert issue == report.issue_reports[0][i]


def test_invalid_getitem():
    with pytest.raises(IndexError):
        test = testdata.DETECTED_ISSUES_RESPONSE_OBJECT[1337]


def test_valid_setitem():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    resp[0] = "foo"
    assert resp.issue_reports[0] == "foo"


def test_report_valid_setitem():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    resp.issue_reports[0][0] = "foo"
    assert resp.issue_reports[0][0] == "foo"


def test_invalid_setitem():
    with pytest.raises(TypeError):
        # string key on list access
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issue_reports["foo"] = "bar"


def test_report_invalid_setitem():
    with pytest.raises(TypeError):
        # string key on list access
        testdata.DETECTED_ISSUES_RESPONSE_OBJECT.issue_reports[0]["foo"] = "bar"


def test_valid_delete():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    del resp[0]
    assert resp.issue_reports == []


def test_valid_report_delete():
    resp = deepcopy(testdata.DETECTED_ISSUES_RESPONSE_OBJECT)
    del resp[0][0]
    assert resp.issue_reports[0].issues == []


def test_invalid_delete():
    with pytest.raises(IndexError):
        del testdata.DETECTED_ISSUES_RESPONSE_OBJECT[1337]


def test_invalid_report_delete():
    with pytest.raises(IndexError):
        del testdata.DETECTED_ISSUES_RESPONSE_OBJECT[0][100]
