import json
from copy import deepcopy

import pytest

from pythx.models.exceptions import ResponseValidationError
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
    with pytest.raises(ResponseValidationError):
        AnalysisListResponse.from_json("[]")


def test_analysis_list_from_empty_json():
    with pytest.raises(ResponseValidationError):
        AnalysisListResponse.from_json("{}")


def test_analysis_list_from_valid_dict():
    resp = AnalysisListResponse.from_dict(testdata.ANALYSIS_LIST_RESPONSE_DICT)
    assert len(resp.analyses) == 2
    for i, analysis in enumerate(resp.analyses):
        assert_analysis_data(
            testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"][i], analysis
        )


def test_analysis_list_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        AnalysisListResponse.from_dict("[]")


def test_analysis_list_from_empty_dict():
    with pytest.raises(ResponseValidationError):
        AnalysisListResponse.from_dict({})


def test_analysis_list_to_dict():
    d = testdata.ANALYSIS_LIST_RESPONSE_OBJECT.to_dict()
    assert d == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_analysis_list_to_json():
    json_str = testdata.ANALYSIS_LIST_RESPONSE_OBJECT.to_json()
    assert json.loads(json_str) == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_iteration():
    uuids = (testdata.UUID_1, testdata.UUID_2)
    # XXX: Don't use zip here to make sure __iter__ returns
    for idx, analysis in enumerate(testdata.ANALYSIS_LIST_RESPONSE_OBJECT):
        assert uuids[idx] == analysis.uuid


def test_valid_getitem():
    for idx, analysis in list(
        enumerate(testdata.ANALYSIS_LIST_RESPONSE_OBJECT.analyses)
    ):
        assert testdata.ANALYSIS_LIST_RESPONSE_OBJECT[idx] == analysis


def test_invalid_getitem_index():
    with pytest.raises(IndexError):
        testdata.ANALYSIS_LIST_RESPONSE_OBJECT[1337]


def test_oob_getitem_slice():
    testdata.ANALYSIS_LIST_RESPONSE_OBJECT[1337:9001] == []


def test_valid_delitem():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    del analysis_list[0]
    assert analysis_list.analyses == testdata.ANALYSIS_LIST_RESPONSE_OBJECT.analyses[1:]
    assert analysis_list.total == testdata.ANALYSIS_LIST_RESPONSE_OBJECT.total - 1
    assert len(analysis_list) == testdata.ANALYSIS_LIST_RESPONSE_OBJECT.total - 1


def test_invalid_delitem():
    with pytest.raises(IndexError):
        del testdata.ANALYSIS_LIST_RESPONSE_OBJECT[1337]


def test_valid_setitem():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    analysis_list[0] = "foo"
    assert analysis_list.analyses[0] == "foo"
    assert analysis_list[0] == "foo"
    assert len(analysis_list.analyses) == len(
        testdata.ANALYSIS_LIST_RESPONSE_OBJECT.analyses
    )


def test_invalid_setitem():
    with pytest.raises(IndexError):
        testdata.ANALYSIS_LIST_RESPONSE_OBJECT[1337] = "foo"


def test_reversed():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    assert list(reversed(analysis_list)) == list(
        reversed(testdata.ANALYSIS_LIST_RESPONSE_OBJECT.analyses)
    )
    assert analysis_list.total == testdata.ANALYSIS_LIST_RESPONSE_OBJECT.total


def test_valid_object_contains():
    assert testdata.ANALYSIS_OBJECT in testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_valid_uuid_contains():
    assert testdata.ANALYSIS_OBJECT.uuid in testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_contains_error():
    with pytest.raises(ValueError):
        1 in testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_invalid_object_contains():
    analysis = deepcopy(testdata.ANALYSIS_OBJECT)
    analysis.uuid = "something else"
    assert not analysis in testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_invalid_uuid_contains():
    assert not "foo" in testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_list_not_equals():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    analysis_list.total = 0
    assert analysis_list != testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_nested_analysis_not_equals():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    analysis_list.analyses[0].uuid = "foo"
    assert analysis_list != testdata.ANALYSIS_LIST_RESPONSE_OBJECT


def test_valid_equals():
    analysis_list = deepcopy(testdata.ANALYSIS_LIST_RESPONSE_OBJECT)
    assert analysis_list == testdata.ANALYSIS_LIST_RESPONSE_OBJECT
