import json
from copy import copy

import pytest

from pythx.models.exceptions import ResponseDecodeError, ResponseValidationError
from pythx.models.response import AnalysisListResponse
from pythx.models.response.analysis import Analysis
from pythx.models.util import serialize_api_timestamp


from . import common as testdata


def assert_analysis_data(expected, analysis: Analysis):
    assert expected["apiVersion"] == analysis.api_version
    assert expected["maruVersion"] == analysis.maru_version
    assert expected["mythrilVersion"] == analysis.mythril_version
    assert expected["maestroVersion"] == analysis.maestro_version
    assert expected["harveyVersion"] == analysis.harvey_version
    assert expected["queueTime"] == analysis.queue_time
    assert expected["runTime"] == analysis.run_time
    assert expected["status"] == analysis.status
    assert expected["submittedAt"] == serialize_api_timestamp(analysis.submitted_at)
    assert expected["submittedBy"] == analysis.submitted_by
    assert expected["uuid"] == analysis.uuid


def test_analysis_list_from_valid_json():
    resp = AnalysisListResponse.from_json(
        json.dumps(testdata.ANALYSIS_LIST_RESPONSE_DICT)
    )
    assert len(resp.analyses) == 2
    for i, analysis in enumerate(resp.analyses):
        assert_analysis_data(
            testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"][i], analysis
        )


def test_analysis_list_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AnalysisListResponse.from_json("[]")


def test_analysis_list_from_empty_json():
    with pytest.raises(ResponseDecodeError):
        AnalysisListResponse.from_json("{}")


def test_analysis_list_from_valid_dict():
    resp = AnalysisListResponse.from_dict(testdata.ANALYSIS_LIST_RESPONSE_DICT)
    assert len(resp.analyses) == 2
    for i, analysis in enumerate(resp.analyses):
        assert_analysis_data(
            testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"][i], analysis
        )


def test_analysis_list_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        AnalysisListResponse.from_dict("[]")


def test_analysis_list_from_empty_dict():
    with pytest.raises(ResponseDecodeError):
        AnalysisListResponse.from_dict({})


def test_analysis_list_to_dict():
    d = testdata.ANALYSIS_LIST_RESPONSE_OBJECT.to_dict()
    assert d == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_analysis_list_to_json():
    json_str = testdata.ANALYSIS_LIST_RESPONSE_OBJECT.to_json()
    assert json.loads(json_str) == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_valid_validate():
    testdata.ANALYSIS_LIST_RESPONSE_OBJECT.validate()


def test_invalid_total_validate():
    resp = copy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    resp.total = -1
    with pytest.raises(ResponseValidationError):
        resp.validate()
