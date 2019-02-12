from pythx.api.handler import APIHandler
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

HANDLER = APIHandler()


def assert_request_dict(d):
    assert d.get("method") is not None
    assert d.get("payload") is not None
    assert d.get("headers") is not None
    assert d.get("url") is not None


@pytest.mark.parametrize(
    "request_obj",
    [
        TEST_ANALYSIS_LIST,
        TEST_ANALYSIS_STATUS,
        TEST_ANALYSIS_SUBMISSION,
        TEST_AUTH_LOGIN,
        TEST_AUTH_LOGOUT,
        TEST_AUTH_REFRESH,
    ],
)
def test_request_dicts(request_obj):
    req_dict = HANDLER.assemble_request(request_obj)
    assert_request_dict(req_dict)
    assert req_dict["method"] == request_obj.method
    assert req_dict["payload"] == request_obj.payload()
    assert req_dict["headers"] == {}
    assert request_obj.endpoint in req_dict["url"]
