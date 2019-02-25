import json

import pytest

from . import common as testdata
from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import DetectedIssuesRequest


def test_analysis_issues_request_from_valid_json():
    req = DetectedIssuesRequest.from_json(json.dumps(testdata.DETECTED_ISSUES_REQUEST_DICT))
    assert req.uuid == testdata.UUID_1
    assert req.method == "GET"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}


def test_analysis_issues_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        DetectedIssuesRequest.from_json("{}")


def test_analysis_issues_request_from_valid_dict():
    req = DetectedIssuesRequest.from_dict(testdata.DETECTED_ISSUES_REQUEST_DICT)
    assert req.uuid == testdata.UUID_1


def test_analysis_issues_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        DetectedIssuesRequest.from_dict({})


def test_analysis_issues_request_to_json():
    assert json.loads(testdata.DETECTED_ISSUES_REQUEST_OBJECT.to_json()) == testdata.DETECTED_ISSUES_REQUEST_DICT


def test_analysis_issues_request_to_dict():
    assert testdata.DETECTED_ISSUES_REQUEST_OBJECT.to_dict() == testdata.DETECTED_ISSUES_REQUEST_DICT


def test_validate():
    testdata.DETECTED_ISSUES_REQUEST_OBJECT.validate()
