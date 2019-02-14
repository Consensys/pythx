import json

import pytest

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import DetectedIssuesRequest

UUID = "70c06039-b5d9-4556-85cb-67633bef5b99"
ISSUES = {"uuid": UUID}
ISSUES_REQUEST = DetectedIssuesRequest(uuid=UUID)


def test_analysis_issues_request_from_valid_json():
    req = DetectedIssuesRequest.from_json(json.dumps(ISSUES))
    assert req.uuid == UUID
    assert req.method == "GET"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}


def test_analysis_issues_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        DetectedIssuesRequest.from_json("{}")


def test_analysis_issues_request_from_valid_dict():
    req = DetectedIssuesRequest.from_dict(ISSUES)
    assert req.uuid == UUID


def test_analysis_issues_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        DetectedIssuesRequest.from_dict({})


def test_analysis_issues_request_to_json():
    assert json.loads(ISSUES_REQUEST.to_json()) == ISSUES


def test_analysis_issues_request_to_dict():
    assert ISSUES_REQUEST.to_dict() == ISSUES


def test_validate():
    ISSUES_REQUEST.validate()
