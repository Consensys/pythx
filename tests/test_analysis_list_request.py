import json

import dateutil.parser
import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AnalysisListRequest

from . import common as testdata


def assert_analysis_list_request(req):
    assert req.offset == testdata.OFFSET
    assert req.date_from.isoformat() == testdata.DATE_FROM
    assert req.date_to.isoformat() == testdata.DATE_TO
    assert req.payload == {}
    assert req.method == "GET"
    assert req.parameters == testdata.ANALYSIS_LIST_REQUEST_DICT
    assert req.headers == {}


def test_analysis_list_request_from_valid_json():
    req = AnalysisListRequest.from_json(json.dumps(testdata.ANALYSIS_LIST_REQUEST_DICT))
    assert_analysis_list_request(req)


def test_analysis_list_request_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AnalysisListRequest.from_json("{}")


def test_analysis_list_request_from_valid_dict():
    req = AnalysisListRequest.from_dict(testdata.ANALYSIS_LIST_REQUEST_DICT)
    assert_analysis_list_request(req)


def test_analysis_list_request_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AnalysisListRequest.from_dict({})


def test_analysis_list_request_to_json():
    assert (
        json.loads(testdata.ANALYSIS_LIST_REQUEST_OBJECT.to_json())
        == testdata.ANALYSIS_LIST_REQUEST_DICT
    )


def test_analysis_list_request_to_dict():
    assert (
        testdata.ANALYSIS_LIST_REQUEST_OBJECT.to_dict()
        == testdata.ANALYSIS_LIST_REQUEST_DICT
    )
