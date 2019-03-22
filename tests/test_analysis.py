import json
from copy import copy

import dateutil.parser
import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import Analysis, AnalysisStatus
from pythx.models.util import deserialize_api_timestamp, serialize_api_timestamp

from . import common as testdata


def assert_analysis(analysis):
    assert analysis.uuid == testdata.UUID_1
    assert analysis.api_version == testdata.API_VERSION_1
    assert analysis.maru_version == testdata.MARU_VERSION_1
    assert analysis.mythril_version == testdata.MYTHRIL_VERSION_1
    assert analysis.maestro_version == testdata.MAESTRO_VERSION_1
    assert analysis.harvey_version == testdata.HARVEY_VERSION_1
    assert analysis.queue_time == testdata.QUEUE_TIME_1
    assert analysis.run_time == 0  # default value
    assert analysis.status == AnalysisStatus(testdata.STATUS_1)
    assert analysis.submitted_at == dateutil.parser.parse(testdata.SUBMITTED_AT_1)
    assert analysis.submitted_by == testdata.SUBMITTED_BY_1


def test_analysis_from_valid_json():
    analysis = Analysis.from_json(json.dumps(testdata.ANALYSIS_DICT))
    assert_analysis(analysis)


def test_analysis_to_json():
    assert json.loads(testdata.ANALYSIS_OBJECT.to_json()) == testdata.ANALYSIS_DICT


def test_analysis_to_dict():
    assert testdata.ANALYSIS_OBJECT.to_dict() == testdata.ANALYSIS_DICT


def test_analysis_propagate_error_field():
    analysis = copy(testdata.ANALYSIS_OBJECT)
    # add optional error field
    analysis.error = testdata.ERROR
    analysis_dict = analysis.to_dict()
    analysis_dict["error"] == testdata.ERROR


def test_analysis_from_valid_dict():
    analysis = Analysis.from_dict(testdata.ANALYSIS_DICT)
    assert_analysis(analysis)


def test_repr():
    analysis_repr = repr(testdata.ANALYSIS_OBJECT)
    assert testdata.ANALYSIS_OBJECT.uuid in analysis_repr
    testdata.ANALYSIS_OBJECT.status in analysis_repr
