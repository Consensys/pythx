import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import AnalysisListResponse
from pythx.models.response.analysis import Analysis
from pythx.models.util import serialize_api_timestamp

API_VERSION_1 = "v1.3.0"
API_VERSION_2 = "v1.2.0"
MARU_VERSION_1 = "v0.2.0"
MARU_VERSION_2 = "v0.1.0"
MYTHRIL_VERSION_1 = "0.19.11"
MYTHRIL_VERSION_2 = "0.19.10"
QUEUE_TIME_1 = 1
QUEUE_TIME_2 = 2
RUN_TIME_1 = 300
RUN_TIME_2 = 200
STATUS_1 = "Running"
STATUS_2 = "Finished"
SUBMITTED_AT_1 = "2019-01-10T01:29:38.410Z"
SUBMITTED_AT_2 = "2019-01-09T01:29:38.410Z"
SUBMITTED_BY_1 = "000008544b0aa00010a91111"
SUBMITTED_BY_2 = "000008544b0aa00010a91111"
UUID_1 = "0680a1e2-b908-4c9a-a15b-636ef9b61486"
UUID_2 = "0680a1e2-b904-4c9a-a15b-636ef9b61486"
VALID_LIST = [
    {
        "uuid": UUID_1,
        "apiVersion": API_VERSION_1,
        "maruVersion": MARU_VERSION_1,
        "mythrilVersion": MYTHRIL_VERSION_1,
        "queueTime": QUEUE_TIME_1,
        "runTime": RUN_TIME_1,
        "status": STATUS_1,
        "submittedAt": SUBMITTED_AT_1,
        "submittedBy": SUBMITTED_BY_1,
    },
    {
        "uuid": UUID_2,
        "apiVersion": API_VERSION_2,
        "maruVersion": MARU_VERSION_2,
        "mythrilVersion": MYTHRIL_VERSION_2,
        "queueTime": QUEUE_TIME_2,
        "runTime": RUN_TIME_2,
        "status": STATUS_2,
        "submittedAt": SUBMITTED_AT_2,
        "submittedBy": SUBMITTED_BY_2,
    },
]

VALID_LIST_RESPONSE = AnalysisListResponse(
    analyses=[
        Analysis(
            uuid=UUID_1,
            api_version=API_VERSION_1,
            maru_version=MARU_VERSION_1,
            mythril_version=MYTHRIL_VERSION_1,
            queue_time=QUEUE_TIME_1,
            run_time=RUN_TIME_1,
            status=STATUS_1,
            submitted_at=SUBMITTED_AT_1,
            submitted_by=SUBMITTED_BY_1,
        ),
        Analysis(
            uuid=UUID_2,
            api_version=API_VERSION_2,
            maru_version=MARU_VERSION_2,
            mythril_version=MYTHRIL_VERSION_2,
            queue_time=QUEUE_TIME_2,
            run_time=RUN_TIME_2,
            status=STATUS_2,
            submitted_at=SUBMITTED_AT_2,
            submitted_by=SUBMITTED_BY_2,
        ),
    ]
)


def assert_analysis_data(expected, analysis: Analysis):
    assert expected["apiVersion"] == analysis.api_version
    assert expected["maruVersion"] == analysis.maru_version
    assert expected["mythrilVersion"] == analysis.mythril_version
    assert expected["queueTime"] == analysis.queue_time
    assert expected["runTime"] == analysis.run_time
    assert expected["status"] == analysis.status
    assert expected["submittedAt"] == serialize_api_timestamp(analysis.submitted_at)
    assert expected["submittedBy"] == analysis.submitted_by
    assert expected["uuid"] == analysis.uuid


def test_analysis_list_from_valid_json():
    resp = AnalysisListResponse.from_json(json.dumps(VALID_LIST))
    assert len(resp.analyses) == 2
    for i, analysis in enumerate(resp.analyses):
        assert_analysis_data(VALID_LIST[i], analysis)


def test_analysis_list_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AnalysisListResponse.from_json("{}")


def test_analysis_list_from_empty_json():
    resp = AnalysisListResponse.from_json("[]")
    assert len(resp.analyses) == 0


def test_analysis_list_from_valid_dict():
    resp = AnalysisListResponse.from_dict(VALID_LIST)
    assert len(resp.analyses) == 2
    for i, analysis in enumerate(resp.analyses):
        assert_analysis_data(VALID_LIST[i], analysis)


def test_analysis_list_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        # list of dicts expected
        AnalysisListResponse.from_dict("{}")


def test_analysis_list_from_empty_dict():
    resp = AnalysisListResponse.from_dict([])
    assert len(resp.analyses) == 0


def test_analysis_list_to_dict():
    d = VALID_LIST_RESPONSE.to_dict()
    assert d == VALID_LIST


def test_analysis_list_to_json():
    json_str = VALID_LIST_RESPONSE.to_json()
    assert json.loads(json_str) == VALID_LIST
