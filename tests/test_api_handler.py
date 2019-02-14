import json
from datetime import datetime

import dateutil.parser
import pytest

from pythx import config
from pythx.api.handler import APIHandler
from pythx.middleware.base import BaseMiddleware
from pythx.models import request as reqmodels
from pythx.models import response as respmodels


class TestMiddleware(BaseMiddleware):
    def process_request(self, req):
        req["test"] = "test"
        return req

    def process_response(self, resp):
        resp.test = "test"
        return resp


TEST_ANALYSIS_LIST = reqmodels.AnalysisListRequest(
    offset=0, date_from=datetime.now(), date_to=datetime.now()
)
TEST_ANALYSIS_SUBMISSION = reqmodels.AnalysisSubmissionRequest(bytecode="0x")
TEST_ANALYSIS_STATUS = reqmodels.AnalysisStatusRequest(uuid="test")
TEST_DETECTED_ISSUES = reqmodels.DetectedIssuesRequest(uuid="test")
TEST_AUTH_LOGIN = reqmodels.AuthLoginRequest(eth_address="0x0", password="lelwat")
TEST_AUTH_LOGOUT = reqmodels.AuthLogoutRequest()
TEST_AUTH_REFRESH = reqmodels.AuthRefreshRequest(access_token="", refresh_token="")

TEST_LIST_RESPONSE = {
    "analyses": [
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
    ],
    "total": 2,
}
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

STAGING_HANDLER = APIHandler(middlewares=[TestMiddleware()], staging=True)
PROD_HANDLER = APIHandler(middlewares=[TestMiddleware()])


def assert_request_dict_keys(d):
    assert d.get("method") is not None
    assert d.get("payload") is not None
    assert d.get("headers") is not None
    assert d.get("url") is not None
    assert d.get("params") is not None


def assert_request_dict_content(d, request_obj):
    assert d["method"] == request_obj.method
    assert d["payload"] == request_obj.payload
    assert d["headers"] == request_obj.headers
    assert d["params"] == request_obj.parameters
    assert request_obj.endpoint in d["url"]
    # check middleware request processing
    assert d["test"] == "test"


def assert_response_middleware_hook(model):
    assert model.test == "test"


@pytest.mark.parametrize(
    "request_obj",
    [
        TEST_ANALYSIS_LIST,
        TEST_DETECTED_ISSUES,
        TEST_ANALYSIS_STATUS,
        TEST_ANALYSIS_SUBMISSION,
        TEST_AUTH_LOGIN,
        TEST_AUTH_LOGOUT,
        TEST_AUTH_REFRESH,
    ],
)
def test_request_dicts(request_obj):
    req_dict = PROD_HANDLER.assemble_request(request_obj)
    assert_request_dict_keys(req_dict)
    assert_request_dict_content(req_dict, request_obj)
    assert req_dict["url"].startswith(config["endpoints"]["production"])

    req_dict = STAGING_HANDLER.assemble_request(request_obj)
    assert_request_dict_keys(req_dict)
    assert_request_dict_content(req_dict, request_obj)
    assert req_dict["url"].startswith(config["endpoints"]["staging"])


def test_middleware_default_empty():
    assert APIHandler().middlewares == []


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
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_LIST_RESPONSE), respmodels.AnalysisListResponse
    )
    assert_response_middleware_hook(model)
    for i, analysis in enumerate(model.analyses):
        response_obj = TEST_LIST_RESPONSE["analyses"][i]
        assert_analysis(analysis, response_obj)


def test_parse_analysis_status_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_STATUS_RESPONSE), respmodels.AnalysisStatusResponse
    )
    assert_response_middleware_hook(model)
    assert_analysis(model.analysis, TEST_STATUS_RESPONSE)


def test_parse_analysis_submission_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_SUBMISSION_RESPONSE), respmodels.AnalysisSubmissionResponse
    )
    assert_response_middleware_hook(model)
    assert model.analysis.api_version == TEST_SUBMISSION_RESPONSE["apiVersion"]
    assert model.analysis.maru_version == TEST_SUBMISSION_RESPONSE["maruVersion"]
    assert model.analysis.mythril_version == TEST_SUBMISSION_RESPONSE["mythrilVersion"]
    assert model.analysis.queue_time == TEST_SUBMISSION_RESPONSE["queueTime"]
    assert model.analysis.status.title() == TEST_SUBMISSION_RESPONSE["status"]
    assert model.analysis.submitted_at == dateutil.parser.parse(
        TEST_SUBMISSION_RESPONSE["submittedAt"]
    )
    assert model.analysis.submitted_by == TEST_SUBMISSION_RESPONSE["submittedBy"]
    assert model.analysis.uuid == TEST_SUBMISSION_RESPONSE["uuid"]


def test_parse_detected_issues_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_ISSUES_RESPONSE), respmodels.DetectedIssuesResponse
    )
    assert_response_middleware_hook(model)
    assert model.issues[0].to_dict() == TEST_ISSUES_RESPONSE[0]["issues"][0]
    assert model.source_type == TEST_ISSUES_RESPONSE[0]["sourceType"]
    assert model.source_format == TEST_ISSUES_RESPONSE[0]["sourceFormat"]
    assert model.source_list == TEST_ISSUES_RESPONSE[0]["sourceList"]
    assert model.meta_data == TEST_ISSUES_RESPONSE[0]["meta"]


def test_parse_login_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_LOGIN_RESPONSE), respmodels.AuthLoginResponse
    )
    assert_response_middleware_hook(model)
    assert model.access_token == TEST_LOGIN_RESPONSE["access"]
    assert model.refresh_token == TEST_LOGIN_RESPONSE["refresh"]


def test_parse_refresh_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(TEST_LOGIN_RESPONSE), respmodels.AuthRefreshResponse
    )
    assert_response_middleware_hook(model)
    assert model.access_token == TEST_LOGIN_RESPONSE["access"]
    assert model.refresh_token == TEST_LOGIN_RESPONSE["refresh"]


def test_parse_logout_response():
    model = PROD_HANDLER.parse_response(
        (json.dumps(TEST_LOGOUT_RESPONSE)), respmodels.AuthLogoutResponse
    )
    assert_response_middleware_hook(model)
    assert model.to_dict() == {}
    assert model.to_json() == "{}"
