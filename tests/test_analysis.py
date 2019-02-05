import json

import dateutil.parser
import pytest

from pythx.core.exceptions import ResponseDecodeError
from pythx.core.response.analysis import Analysis, AnalysisStatus


VALID_INPUT_JSON_TPL = """{{
    "apiVersion": "{api_version}",
    "maruVersion": "{maru_version}",
    "mythrilVersion": "{mythril_version}",
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
QUEUE_TIME = 0
STATUS = "Queued"
SUBMITTED_AT = "2019-01-10T01:29:38.410Z"
SUBMITTED_BY = "000008544b0aa00010a91111"


def test_analysis_from_valid_json():
    input_str = VALID_INPUT_JSON_TPL.format(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
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
    assert analysis.queue_time == QUEUE_TIME
    assert analysis.run_time == 0  # default value
    assert analysis.status == AnalysisStatus.QUEUED
    assert analysis.submitted_at == dateutil.parser.parse(SUBMITTED_AT)
    assert analysis.submitted_by == SUBMITTED_BY


def test_analysis_invalid_json():
    with pytest.raises(ResponseDecodeError):
        Analysis.from_json("{}")


def test_analysis_to_valid_json():
    analysis = Analysis(
        uuid=UUID,
        api_version=API_VERSION,
        maru_version=MARU_VERSION,
        mythril_version=MYTHRIL_VERSION,
        queue_time=QUEUE_TIME,
        status=STATUS,
        submitted_at=SUBMITTED_AT,
        submitted_by=SUBMITTED_BY,
    )
    assert json.loads(analysis.to_json()) == {
        "uuid": UUID,
        "api_version": API_VERSION,
        "maru_version": MARU_VERSION,
        "mythril_version": MYTHRIL_VERSION,
        "queue_time": QUEUE_TIME,
        "run_time": 0,
        "status": STATUS,
        "submitted_at": "2019-01-10T01:29:38.410000+00:00",  # Python isotime
        "submitted_by": SUBMITTED_BY,
    }
