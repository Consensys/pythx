from pythx.api.handler import APIHandler
from pythx.core.response import models as respmodels
import json
import pytest
import dateutil.parser


TEST_LIST_RESPONSE = [
    {
        "apiVersion": "v1.3.0",
        "maruVersion": "v0.2.0",
        "mythrilVersion": "0.19.11",
        "queueTime": 1,
        "runTime": 300,
        "status": "Running",
        "submittedAt": "2019-01-10T01:29:38.410Z",
        "submittedBy": "000008544b0aa00010a91111",
        "uuid": "0680a1e2-b908-4c9a-a15b-636ef9b61486",
    },
    {
        "apiVersion": "v1.3.0",
        "maruVersion": "v0.2.0",
        "mythrilVersion": "0.19.11",
        "queueTime": 0,
        "runTime": 0,
        "status": "Finished",
        "submittedAt": "2019-01-10T01:28:56.551Z",
        "submittedBy": "000008544b0aa00010a91111",
        "uuid": "78e3e82b-869d-4df1-8acf-cb1161281b71",
    },
]
TEST_STATUS_RESPONSE = {
    "apiVersion": "string",
    "mythrilVersion": "string",
    "maruVersion": "string",
    "queueTime": 0,
    "runTime": 0,
    "status": "Queued",
    "submittedAt": "2019-02-04T16:04:39Z",
    "submittedBy": "string",
    "uuid": "string",
}
TEST_SUBMISSION_RESPONSE = {
    "apiVersion": "v1.3.0",
    "maruVersion": "v0.2.0",
    "mythrilVersion": "0.19.11",
    "queueTime": 0,
    "status": "Queued",
    "submittedAt": "2019-01-10T01:29:38.410Z",
    "submittedBy": "000008544b0aa00010a91111",
    "uuid": "0680a1e2-b908-4c9a-a15b-636ef9b61486",
}
TEST_ISSUES_RESPONSE = [
    {
        "issues": [
            {
                "swcID": "SWC-103",
                "swcTitle": "FloatingPragma",
                "description": {
                    "head": "A floating pragma is set.",
                    "tail": 'It is recommended to make a conscious choice on what version of Solidity is used for compilation. Currently any version equal or grater than "0.4.24" is allowed.',
                },
                "severity": "Low",
                "locations": [
                    {
                        "sourceMap": "48:1:0",
                        "sourceType": "raw_bytecode",
                        "sourceFormat": "evm-byzantium-bytecode",
                        "sourceList": ["/test/my-super-safe-contract.sol"],
                    }
                ],
                "extra": {},
            }
        ],
        "sourceType": "solidity-file",
        "sourceFormat": "text",
        "sourceList": ["/test/my-super-safe-contract.sol"],
        "meta": {},
    }
]
TEST_LOGIN_RESPONSE = {"access": "string", "refresh": "string"}
TEST_REFRESH_RESPONSE = {"access": "string", "refresh": "string"}
TEST_LOGOUT_RESPONSE = {}


def assert_analysis(analysis, data):
    assert analysis.api_version == data["apiVersion"]
    assert analysis.maru_version == data["maruVersion"]
    assert analysis.mythril_version == data["mythrilVersion"]
    assert analysis.run_time == data["runTime"]
    assert analysis.queue_time == data["queueTime"]
    assert analysis.status.title() == data["status"]
    assert analysis.submitted_at == dateutil.parser.parse(data["submittedAt"])
    assert analysis.submitted_by == data["submittedBy"]
    assert analysis.uuid == data["uuid"]


def test_parse_analysis_list_response():
    handler = APIHandler()
    model = handler.parse_response(
        json.dumps(TEST_LIST_RESPONSE), respmodels.AnalysisListResponse
    )
    for i, analysis in enumerate(model.analyses):
        response_obj = TEST_LIST_RESPONSE[i]
        assert_analysis(analysis, response_obj)


def test_parse_analysis_status_response():
    handler = APIHandler()
    model = handler.parse_response(
        json.dumps(TEST_STATUS_RESPONSE), respmodels.AnalysisStatusResponse
    )
    assert_analysis(model.analysis, TEST_STATUS_RESPONSE)


def test_parse_analysis_submission_response():
    handler = APIHandler()
    model = handler.parse_response(json.dumps(TEST_SUBMISSION_RESPONSE), respmodels.AnalysisSubmissionResponse)
    assert model.analysis.api_version == TEST_SUBMISSION_RESPONSE["apiVersion"]
    assert model.analysis.maru_version == TEST_SUBMISSION_RESPONSE["maruVersion"]
    assert model.analysis.mythril_version == TEST_SUBMISSION_RESPONSE["mythrilVersion"]
    assert model.analysis.queue_time == TEST_SUBMISSION_RESPONSE["queueTime"]
    assert model.analysis.status.title() == TEST_SUBMISSION_RESPONSE["status"]
    assert model.analysis.submitted_at == dateutil.parser.parse(TEST_SUBMISSION_RESPONSE["submittedAt"])
    assert model.analysis.submitted_by == TEST_SUBMISSION_RESPONSE["submittedBy"]
    assert model.analysis.uuid == TEST_SUBMISSION_RESPONSE["uuid"]

def test_parse_detected_issues_response():
    handler = APIHandler()
    model = handler.parse_response(json.dumps(TEST_ISSUES_RESPONSE), respmodels.DetectedIssuesResponse)
    assert model.issues[0].to_dict() == TEST_ISSUES_RESPONSE[0]["issues"][0]
    assert model.source_type == TEST_ISSUES_RESPONSE[0]["sourceType"]
    assert model.source_format == TEST_ISSUES_RESPONSE[0]["sourceFormat"]
    assert model.source_list == TEST_ISSUES_RESPONSE[0]["sourceList"]
    assert model.meta_data == TEST_ISSUES_RESPONSE[0]["meta"]

def test_parse_login_response():
    handler = APIHandler()
    model = handler.parse_response(json.dumps(TEST_LOGIN_RESPONSE), respmodels.AuthLoginResponse)
    assert model.access_token == TEST_LOGIN_RESPONSE["access"]
    assert model.refresh_token == TEST_LOGIN_RESPONSE["refresh"]

def test_parse_refresh_response():
    handler = APIHandler()
    model = handler.parse_response(json.dumps(TEST_LOGIN_RESPONSE), respmodels.AuthRefreshResponse)
    assert model.access_token == TEST_LOGIN_RESPONSE["access"]
    assert model.refresh_token == TEST_LOGIN_RESPONSE["refresh"]

def test_parse_logout_response():
    handler = APIHandler()
    model = handler.parse_response((json.dumps(TEST_LOGOUT_RESPONSE)), respmodels.AuthLogoutResponse)
    assert model.to_dict() == {}
    assert model.to_json() == "{}"
