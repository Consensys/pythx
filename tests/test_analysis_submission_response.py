import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import Analysis, AnalysisSubmissionResponse
from pythx.models.util import serialize_api_timestamp

UUID_1 = "0680a1e2-b908-4c9a-a15b-636ef9b61486"
API_VERSION_1 = "v1.3.0"
MARU_VERSION_1 = "v0.2.0"
MYTHRIL_VERSION_1 = "0.19.11"
MAESTRO_VERSION_1 = "v1.1.4"
HARVEY_VERSION_1 = "0.0.8"
QUEUE_TIME_1 = 1
RUN_TIME_1 = 300
STATUS_1 = "Running"
SUBMITTED_AT_1 = "2019-01-10T01:29:38.410Z"
SUBMITTED_BY_1 = "000008544b0aa00010a91111"
VALID_ANALYSIS_DICT = {
    "uuid": UUID_1,
    "apiVersion": API_VERSION_1,
    "maruVersion": MARU_VERSION_1,
    "mythrilVersion": MYTHRIL_VERSION_1,
    "maestroVersion": MAESTRO_VERSION_1,
    "harveyVersion": HARVEY_VERSION_1,
    "queueTime": QUEUE_TIME_1,
    "runTime": RUN_TIME_1,
    "status": STATUS_1,
    "submittedAt": SUBMITTED_AT_1,
    "submittedBy": SUBMITTED_BY_1,
}

VALID_SUBMISSION_RESPONSE = AnalysisSubmissionResponse(
    analysis=Analysis(
        uuid=UUID_1,
        api_version=API_VERSION_1,
        maru_version=MARU_VERSION_1,
        mythril_version=MYTHRIL_VERSION_1,
        maestro_version=MAESTRO_VERSION_1,
        harvey_version=HARVEY_VERSION_1,
        queue_time=QUEUE_TIME_1,
        run_time=RUN_TIME_1,
        status=STATUS_1,
        submitted_at=SUBMITTED_AT_1,
        submitted_by=SUBMITTED_BY_1,
    )
)


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
    resp = AnalysisSubmissionResponse.from_json(json.dumps(VALID_ANALYSIS_DICT))
    assert_analysis_data(VALID_ANALYSIS_DICT, resp.analysis)


def test_analysis_list_from_empty_json():
    with pytest.raises(ResponseDecodeError):
        AnalysisSubmissionResponse.from_json("{}")


def test_analysis_list_from_valid_dict():
    resp = AnalysisSubmissionResponse.from_dict(VALID_ANALYSIS_DICT)
    assert_analysis_data(VALID_ANALYSIS_DICT, resp.analysis)


def test_analysis_list_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        # list of dicts expected
        AnalysisSubmissionResponse.from_dict("{}")


def test_analysis_list_from_empty_dict():
    with pytest.raises(ResponseDecodeError):
        AnalysisSubmissionResponse.from_dict({})


def test_analysis_list_to_dict():
    d = VALID_SUBMISSION_RESPONSE.to_dict()
    assert d == VALID_ANALYSIS_DICT


def test_analysis_list_to_json():
    json_str = VALID_SUBMISSION_RESPONSE.to_json()
    assert json.loads(json_str) == VALID_ANALYSIS_DICT
