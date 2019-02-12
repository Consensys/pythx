from pythx.api.handler import APIHandler
from pythx import config
from pythx.core.request import models as reqmodels
from datetime import datetime

import pytest


TEST_ANALYSIS_LIST = reqmodels.AnalysisListRequest(
    offset=0, date_from=datetime.now(), date_to=datetime.now()
)
TEST_ANALYSIS_SUBMISSION = reqmodels.AnalysisSubmissionRequest(bytecode="0x")
TEST_ANALYSIS_STATUS = reqmodels.AnalysisStatusRequest(uuid="test")
TEST_DETECTED_ISSUES = reqmodels.DetectedIssuesRequest(uuid="test")
TEST_AUTH_LOGIN = reqmodels.AuthLoginRequest(
    eth_address="0x0", password="lelwat", user_id="test"
)
TEST_AUTH_LOGOUT = reqmodels.AuthLogoutRequest()
TEST_AUTH_REFRESH = reqmodels.AuthRefreshRequest(access_token="", refresh_token="")

STAGING_HANDLER = APIHandler(staging=True)
PROD_HANDLER = APIHandler()


def assert_request_dict_keys(d):
    assert d.get("method") is not None
    assert d.get("payload") is not None
    assert d.get("headers") is not None
    assert d.get("url") is not None


def assert_request_dict_content(d, request_obj):
    assert d["method"] == request_obj.method
    assert d["payload"] == request_obj.payload()
    assert d["headers"] == {}
    assert request_obj.endpoint in d["url"]


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
