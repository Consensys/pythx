import json

import pytest

from . import common as testdata
from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import AnalysisStatusRequest


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
    with pytest.raises(RequestDecodeError):
        AnalysisStatusRequest.from_json("{}")


def test_analysis_status_request_from_valid_dict():
    req = AnalysisStatusRequest.from_dict(testdata.ANALYSIS_STATUS_REQUEST_DICT)
    assert_status_request(req)


def test_analysis_status_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
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
