import json
from copy import copy

import dateutil.parser
import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import Analysis, AnalysisStatus
from pythx.models.util import deserialize_api_timestamp, serialize_api_timestamp

VALID_INPUT_JSON_TPL = """{{
    "apiVersion": "{api_version}",
    "maruVersion": "{maru_version}",
    "mythrilVersion": "{mythril_version}",
    "maestroVersion": "{maestro_version}",
    "harveyVersion": "{harvey_version}",
    "queueTime": {queue_time},
    "status": "{status}",
    "submittedAt": "{submitted_at}",
    "submittedBy": "{submitted_by}",
    "uuid": "{uuid}"
}}"""

UUID = "0680a1e2-b908-4c9a-a15b-636ef9b61486"
API_VERSION = "v1.3.0"
MARU_VERSION = "v0.2.0"
MYTHRIL_VERSION = "0.19.11"
MAESTRO_VERSION = "v1.1.4"
HARVEY_VERSION = "0.0.8"
QUEUE_TIME = 0
STATUS = "Queued"
SUBMITTED_AT = "2019-01-10T01:29:38.410Z"
SUBMITTED_BY = "000008544b0aa00010a91111"
ERROR = "my test error"
ANALYSIS = Analysis(
    uuid=UUID,
    api_version=API_VERSION,
    maru_version=MARU_VERSION,
    mythril_version=MYTHRIL_VERSION,
    maestro_version=MAESTRO_VERSION,
    harvey_version=HARVEY_VERSION,
    queue_time=QUEUE_TIME,
    status=STATUS,
    submitted_at=SUBMITTED_AT,
    submitted_by=SUBMITTED_BY,
)


def test_analysis_from_valid_json():
    input_str = VALID_INPUT_JSON_TPL.format(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
        maestro_version=MAESTRO_VERSION,
        harvey_version=HARVEY_VERSION,
        queue_time=QUEUE_TIME,
        status=STATUS,
        submitted_at=SUBMITTED_AT,
        submitted_by=SUBMITTED_BY,
    )
    analysis = Analysis.from_json(input_str)
    assert analysis.uuid == UUID
    assert analysis.api_version == API_VERSION
    assert analysis.maru_version == MARU_VERSION
    assert analysis.mythril_version == MYTHRIL_VERSION
    assert analysis.maestro_version == MAESTRO_VERSION
    assert analysis.harvey_version == HARVEY_VERSION
    assert analysis.queue_time == QUEUE_TIME
    assert analysis.run_time == 0  # default value
    assert analysis.status == AnalysisStatus.QUEUED
    assert analysis.submitted_at == dateutil.parser.parse(SUBMITTED_AT)
    assert analysis.submitted_by == SUBMITTED_BY


def test_analysis_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        Analysis.from_json("{}")


def test_analysis_to_json():
    analysis = Analysis(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
        maestro_version=MAESTRO_VERSION,
        harvey_version=HARVEY_VERSION,
        queue_time=QUEUE_TIME,
        status=STATUS,
        submitted_at=SUBMITTED_AT,
        submitted_by=SUBMITTED_BY,
    )
    assert json.loads(analysis.to_json()) == {
        "uuid": UUID,
        "apiVersion": API_VERSION,
        "maruVersion": MARU_VERSION,
        "mythrilVersion": MYTHRIL_VERSION,
        "maestroVersion": MAESTRO_VERSION,
        "harveyVersion": HARVEY_VERSION,
        "queueTime": QUEUE_TIME,
        "runTime": 0,
        "status": STATUS,
        "submittedAt": SUBMITTED_AT,  # Python isotime
        "submittedBy": SUBMITTED_BY,
    }


def test_analysis_to_dict():
    analysis = Analysis(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
        maestro_version=MAESTRO_VERSION,
        harvey_version=HARVEY_VERSION,
        queue_time=QUEUE_TIME,
        status=STATUS,
        submitted_at=SUBMITTED_AT,
        submitted_by=SUBMITTED_BY,
    )
    assert analysis.to_dict() == {
        "uuid": UUID,
        "apiVersion": API_VERSION,
        "maruVersion": MARU_VERSION,
        "mythrilVersion": MYTHRIL_VERSION,
        "maestroVersion": MAESTRO_VERSION,
        "harveyVersion": HARVEY_VERSION,
        "queueTime": QUEUE_TIME,
        "runTime": 0,
        "status": STATUS,
        "submittedAt": SUBMITTED_AT,  # Python isotime
        "submittedBy": SUBMITTED_BY,
    }


def assert_analysis(analysis):
    assert analysis.uuid == UUID
    assert analysis.api_version == API_VERSION
    assert analysis.maru_version == MARU_VERSION
    assert analysis.mythril_version == MYTHRIL_VERSION
    assert analysis.maestro_version == MAESTRO_VERSION
    assert analysis.harvey_version == HARVEY_VERSION
    assert analysis.queue_time == QUEUE_TIME
    assert analysis.run_time == 0  # default value
    assert analysis.status == AnalysisStatus.QUEUED
    assert analysis.submitted_at == deserialize_api_timestamp(SUBMITTED_AT)
    assert analysis.submitted_by == SUBMITTED_BY


def test_analysis_propagate_error_field():
    input_str = VALID_INPUT_JSON_TPL.format(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
        maestro_version=MAESTRO_VERSION,
        harvey_version=HARVEY_VERSION,
        queue_time=QUEUE_TIME,
        status=STATUS,
        submitted_at=SUBMITTED_AT,
        submitted_by=SUBMITTED_BY,
    )
    analysis = copy(ANALYSIS)
    # add optional error field
    analysis.error = ERROR
    analysis_dict = analysis.to_dict()
    analysis_dict["error"] == ERROR


def test_analysis_from_valid_dict():
    input_dict = json.loads(
        VALID_INPUT_JSON_TPL.format(
            uuid=UUID,
            api_version=API_VERSION,
            maru_version=MARU_VERSION,
            mythril_version=MYTHRIL_VERSION,
            maestro_version=MAESTRO_VERSION,
            harvey_version=HARVEY_VERSION,
            queue_time=QUEUE_TIME,
            status=STATUS,
            submitted_at=SUBMITTED_AT,
            submitted_by=SUBMITTED_BY,
        )
    )
    analysis = Analysis.from_dict(input_dict)
    assert_analysis(analysis)


def test_analysis_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        Analysis.from_dict({})


def test_validate():
    ANALYSIS.validate()
