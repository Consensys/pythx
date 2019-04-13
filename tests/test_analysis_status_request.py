import json

import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AnalysisStatusRequest

from . import common as testdata


def assert_status_request(req: AnalysisStatusRequest):
    assert req.uuid == testdata.UUID_1
    assert req.method == "GET"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}


def test_analysis_status_request_from_valid_json():
    req = AnalysisStatusRequest.from_json(
        json.dumps(testdata.ANALYSIS_STATUS_REQUEST_DICT)
    )
    assert_status_request(req)


def test_analysis_status_request_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AnalysisStatusRequest.from_json("{}")


def test_analysis_status_request_from_valid_dict():
    req = AnalysisStatusRequest.from_dict(testdata.ANALYSIS_STATUS_REQUEST_DICT)
    assert_status_request(req)


def test_analysis_status_request_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AnalysisStatusRequest.from_dict({})


def test_analysis_status_request_to_json():
    assert (
        json.loads(testdata.ANALYSIS_STATUS_REQUEST_OBJECT.to_json())
        == testdata.ANALYSIS_STATUS_REQUEST_DICT
    )


def test_analysis_status_request_to_dict():
    assert (
        testdata.ANALYSIS_STATUS_REQUEST_OBJECT.to_dict()
        == testdata.ANALYSIS_STATUS_REQUEST_DICT
    )
