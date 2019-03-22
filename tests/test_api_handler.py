import json
from datetime import datetime

import dateutil.parser
import pytest

from pythx import config
from pythx.api.handler import APIHandler
from pythx.middleware.base import BaseMiddleware
from pythx.models import request as reqmodels
from pythx.models import response as respmodels
from pythx.models.exceptions import PythXAPIError

from . import common as testdata


class TestMiddleware(BaseMiddleware):
    def process_request(self, req):
        req["test"] = "test"
        return req

    def process_response(self, resp):
        resp.test = "test"
        return resp


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
        testdata.ANALYSIS_LIST_REQUEST_OBJECT,
        testdata.DETECTED_ISSUES_REQUEST_OBJECT,
        testdata.ANALYSIS_STATUS_REQUEST_OBJECT,
        testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT,
        testdata.LOGIN_REQUEST_OBJECT,
        testdata.LOGOUT_REQUEST_OBJECT,
        testdata.REFRESH_REQUEST_OBJECT,
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
        json.dumps(testdata.ANALYSIS_LIST_RESPONSE_DICT),
        respmodels.AnalysisListResponse,
    )
    assert_response_middleware_hook(model)
    for i, analysis in enumerate(model.analyses):
        response_obj = testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"][i]
        assert_analysis(analysis, response_obj)


def test_parse_analysis_status_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(testdata.ANALYSIS_STATUS_RESPONSE_DICT),
        respmodels.AnalysisStatusResponse,
    )
    assert_response_middleware_hook(model)
    assert_analysis(model.analysis, testdata.ANALYSIS_STATUS_RESPONSE_DICT)


def test_parse_analysis_submission_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT),
        respmodels.AnalysisSubmissionResponse,
    )
    assert_response_middleware_hook(model)
    assert (
        model.analysis.api_version
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["apiVersion"]
    )
    assert (
        model.analysis.maru_version
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["maruVersion"]
    )
    assert (
        model.analysis.mythril_version
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["mythrilVersion"]
    )
    assert (
        model.analysis.maestro_version
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["maestroVersion"]
    )
    assert (
        model.analysis.harvey_version
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["harveyVersion"]
    )
    assert (
        model.analysis.queue_time
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["queueTime"]
    )
    assert (
        model.analysis.status.title()
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["status"]
    )
    assert model.analysis.submitted_at == dateutil.parser.parse(
        testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["submittedAt"]
    )
    assert (
        model.analysis.submitted_by
        == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["submittedBy"]
    )
    assert model.analysis.uuid == testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT["uuid"]


def test_parse_detected_issues_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(testdata.DETECTED_ISSUES_RESPONSE_DICT),
        respmodels.DetectedIssuesResponse,
    )
    assert_response_middleware_hook(model)
    assert (
        model.issues[0].to_dict()
        == testdata.DETECTED_ISSUES_RESPONSE_DICT[0]["issues"][0]
    )
    assert model.source_type == testdata.DETECTED_ISSUES_RESPONSE_DICT[0]["sourceType"]
    assert (
        model.source_format == testdata.DETECTED_ISSUES_RESPONSE_DICT[0]["sourceFormat"]
    )
    assert model.source_list == testdata.DETECTED_ISSUES_RESPONSE_DICT[0]["sourceList"]
    assert model.meta_data == testdata.DETECTED_ISSUES_RESPONSE_DICT[0]["meta"]


def test_parse_login_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(testdata.LOGIN_RESPONSE_DICT), respmodels.AuthLoginResponse
    )
    assert_response_middleware_hook(model)
    assert model.access_token == testdata.LOGIN_RESPONSE_DICT["access"]
    assert model.refresh_token == testdata.LOGIN_RESPONSE_DICT["refresh"]


def test_parse_refresh_response():
    model = PROD_HANDLER.parse_response(
        json.dumps(testdata.LOGIN_RESPONSE_DICT), respmodels.AuthRefreshResponse
    )
    assert_response_middleware_hook(model)
    assert model.access_token == testdata.LOGIN_RESPONSE_DICT["access"]
    assert model.refresh_token == testdata.LOGIN_RESPONSE_DICT["refresh"]


def test_parse_logout_response():
    model = PROD_HANDLER.parse_response(
        (json.dumps(testdata.LOGOUT_RESPONSE_DICT)), respmodels.AuthLogoutResponse
    )
    assert_response_middleware_hook(model)
    assert model.to_dict() == {}
    assert model.to_json() == "{}"


def test_send_request_successful(requests_mock):
    requests_mock.get("mock://test.com/path", text="resp")
    resp = APIHandler.send_request(
        {
            "method": "GET",
            "headers": {},
            "url": testdata.MOCK_API_URL,
            "payload": {},
            "params": {},
        },
        auth_header={"Authorization": "Bearer foo"},
    )
    assert resp == "resp"
    assert requests_mock.called == 1
    h = requests_mock.request_history[0]
    assert h.method == "GET"
    assert h.url == testdata.MOCK_API_URL
    assert h.headers["Authorization"] == "Bearer foo"


def test_send_request_failure(requests_mock):
    requests_mock.get("mock://test.com/path", text="resp", status_code=400)
    with pytest.raises(PythXAPIError):
        APIHandler.send_request(
            {
                "method": "GET",
                "headers": {},
                "url": testdata.MOCK_API_URL,
                "payload": {},
                "params": {},
            },
            auth_header={"Authorization": "Bearer foo"},
        )

    assert requests_mock.called == 1
    h = requests_mock.request_history[0]
    assert h.method == "GET"
    assert h.url == testdata.MOCK_API_URL
    assert h.headers["Authorization"] == "Bearer foo"


def test_send_request_unauthenticated(requests_mock):
    requests_mock.get("mock://test.com/path", text="resp", status_code=400)
    with pytest.raises(PythXAPIError):
        APIHandler.send_request(
            {
                "method": "GET",
                "headers": {},
                "url": testdata.MOCK_API_URL,
                "payload": {},
                "params": {},
            }
        )

    assert requests_mock.called == 1
    h = requests_mock.request_history[0]
    assert h.method == "GET"
    assert h.url == testdata.MOCK_API_URL
    assert h.headers.get("Authorization") is None
