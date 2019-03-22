import json

import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AnalysisSubmissionRequest

from . import common as testdata


def assert_submission_request(req: AnalysisSubmissionRequest):
    assert req.contract_name == testdata.CONTRACT_NAME
    assert req.bytecode == testdata.BYTECODE
    assert req.source_map == testdata.SOURCE_MAP
    assert req.deployed_bytecode == testdata.DEPLOYED_BYTECODE
    assert req.deployed_source_map == testdata.DEPLOYED_SOURCE_MAP
    assert req.sources == testdata.SOURCES
    assert req.solc_version == testdata.SOLC_VERSION
    assert req.analysis_mode == testdata.ANALYSIS_MODE
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {"data": testdata.ANALYSIS_SUBMISSION_REQUEST_DICT}


def test_analysis_submission_request_from_valid_json():
    req = AnalysisSubmissionRequest.from_json(
        json.dumps(testdata.ANALYSIS_SUBMISSION_REQUEST_DICT)
    )
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AnalysisSubmissionRequest.from_json("{}")


def test_analysis_submission_request_from_valid_dict():
    req = AnalysisSubmissionRequest.from_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_DICT)
    assert_submission_request(req)


def test_analysis_submission_request_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AnalysisSubmissionRequest.from_dict({})


def test_analysis_submission_request_to_json():
    assert (
        json.loads(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT.to_json())
        == testdata.ANALYSIS_SUBMISSION_REQUEST_DICT
    )


def test_analysis_submission_request_to_dict():
    assert (
        testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT.to_dict()
        == testdata.ANALYSIS_SUBMISSION_REQUEST_DICT
    )


def test_analysis_submission_request_bytecode_only():
    req = AnalysisSubmissionRequest(bytecode=testdata.BYTECODE)
    assert req.bytecode == testdata.BYTECODE
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"bytecode": testdata.BYTECODE, "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {
        "bytecode": testdata.BYTECODE,
        "analysisMode": "quick",
    }


def test_analysis_submission_request_source_only():
    req = AnalysisSubmissionRequest(sources=testdata.SOURCES)
    assert req.sources == testdata.SOURCES
    assert req.analysis_mode == "quick"  # default value
    assert req.to_dict() == {"sources": testdata.SOURCES, "analysisMode": "quick"}
    assert json.loads(req.to_json()) == {
        "sources": testdata.SOURCES,
        "analysisMode": "quick",
    }


def test_analysis_submission_request_invalid_mode():
    req = AnalysisSubmissionRequest(bytecode=testdata.BYTECODE, analysis_mode="invalid")
    with pytest.raises(RequestValidationError):
        req.to_dict()


def test_analysis_submission_request_missing_field():
    req = AnalysisSubmissionRequest()
    with pytest.raises(RequestValidationError):
        req.to_dict()
