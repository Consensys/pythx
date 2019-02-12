import json

import pytest

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import AnalysisStatusRequest

UUID = "70c06039-b5d9-4556-85cb-67633bef5b99"
STATUS = {"uuid": UUID}
STATUS_REQUEST = AnalysisStatusRequest(uuid=UUID)


def test_analysis_status_request_from_valid_json():
    req = AnalysisStatusRequest.from_json(json.dumps(STATUS))
    assert req.uuid == UUID


def test_analysis_status_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AnalysisStatusRequest.from_json("{}")


def test_analysis_status_request_from_valid_dict():
    req = AnalysisStatusRequest.from_dict(STATUS)
    assert req.uuid == UUID


def test_analysis_status_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AnalysisStatusRequest.from_dict({})


def test_analysis_status_request_to_json():
    assert json.loads(STATUS_REQUEST.to_json()) == STATUS


def test_analysis_status_request_to_dict():
    assert STATUS_REQUEST.to_dict() == STATUS
