import json
from copy import copy
from datetime import datetime, timedelta

import jwt
import pytest
from dateutil.tz import tzutc

import pythx.models.response as respmodels
from pythx import config
from pythx.api import APIHandler, Client
from pythx.models.exceptions import PythXAPIError, RequestValidationError
from pythx.models.response.analysis import AnalysisStatus
from pythx.models.util import serialize_api_timestamp

from . import common as testdata


class MockAPIHandler(APIHandler):
    def __init__(self, resp):
        super().__init__()
        self.resp = resp

    def send_request(self, *args, **kwargs):
        return json.dumps(self.resp.pop(0))


def get_client(resp_data, logged_in=True, access_expired=False, refresh_expired=False):
    client = Client(
        eth_address="0xdeadbeef",
        password="supersecure",
        handler=MockAPIHandler(resp_data),
    )
    if logged_in:
        # simulate that we're already logged in with tokens
        client.access_token = jwt.encode(
            {
                "exp": datetime(1994, 7, 29, tzinfo=tzutc())
                if access_expired
                else datetime(9999, 1, 1, tzinfo=tzutc())
            },
            "secret",
        )
        client.refresh_token = jwt.encode(
            {
                "exp": datetime(1994, 7, 29, tzinfo=tzutc())
                if refresh_expired
                else datetime(9999, 1, 1, tzinfo=tzutc())
            },
            "secret",
        )

    return client


def test_login():
    client = get_client([testdata.LOGIN_RESPONSE_DICT], logged_in=False)

    assert client.access_token is None
    assert client.refresh_token is None

    resp = client.login()

    assert type(resp) == respmodels.AuthLoginResponse
    assert resp.access_token == testdata.ACCESS_TOKEN_1
    assert resp.refresh_token == testdata.REFRESH_TOKEN_1

    assert client.access_token == testdata.ACCESS_TOKEN_1
    assert client.refresh_token == testdata.REFRESH_TOKEN_1


def test_logout():
    client = get_client([testdata.LOGOUT_RESPONSE_DICT])
    resp = client.logout()

    assert type(resp) == respmodels.AuthLogoutResponse
    assert client.access_token is None
    assert client.refresh_token is None


def test_refresh():
    client = get_client([testdata.REFRESH_RESPONSE_DICT])
    resp = client.refresh()

    assert type(resp) == respmodels.AuthRefreshResponse
    assert resp.access_token == testdata.ACCESS_TOKEN_1
    assert resp.refresh_token == testdata.REFRESH_TOKEN_1
    assert resp.to_dict() == testdata.REFRESH_RESPONSE_DICT

    assert client.access_token == testdata.ACCESS_TOKEN_1
    assert client.refresh_token == testdata.REFRESH_TOKEN_1


def test_analysis_list():
    client = get_client([testdata.ANALYSIS_LIST_RESPONSE_DICT])
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )

    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"])
    assert resp.to_dict() == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_auto_login():
    client = get_client(
        [testdata.LOGIN_RESPONSE_DICT, testdata.ANALYSIS_LIST_RESPONSE_DICT],
        logged_in=False,
    )
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )
    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"])
    assert resp.to_dict() == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_expired_auth_and_refresh_token():
    client = get_client(
        [testdata.LOGIN_RESPONSE_DICT, testdata.ANALYSIS_LIST_RESPONSE_DICT],
        logged_in=True,
        access_expired=True,
        refresh_expired=True,
    )
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )
    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"])
    assert resp.to_dict() == testdata.ANALYSIS_LIST_RESPONSE_DICT


def test_expired_access_token():
    client = get_client(
        [testdata.REFRESH_RESPONSE_DICT, testdata.ANALYSIS_LIST_RESPONSE_DICT],
        logged_in=True,
        access_expired=True,
    )
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )
    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(testdata.ANALYSIS_LIST_RESPONSE_DICT["analyses"])
    assert resp.to_dict() == testdata.ANALYSIS_LIST_RESPONSE_DICT


def assert_analysis(analysis):
    assert analysis.uuid == testdata.UUID_1
    assert analysis.api_version == testdata.API_VERSION_1
    assert analysis.mythril_version == testdata.MYTHRIL_VERSION_1
    assert analysis.maru_version == testdata.MARU_VERSION_1
    assert analysis.run_time == testdata.RUN_TIME_1
    assert analysis.queue_time == testdata.QUEUE_TIME_1
    assert analysis.status == AnalysisStatus(testdata.STATUS_1)
    assert serialize_api_timestamp(analysis.submitted_at) == testdata.SUBMITTED_AT_1
    assert analysis.submitted_by == testdata.SUBMITTED_BY_1


def test_analyze_bytecode():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    resp = client.analyze(bytecode="0xf00")

    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_source_code():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    resp = client.analyze(sources={"foo.sol": {"source": "bar"}})

    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_source_and_bytecode():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    resp = client.analyze(sources={"foo.sol": {"source": "bar"}}, bytecode="0xf00")
    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_missing_data():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    with pytest.raises(RequestValidationError):
        client.analyze()


def test_analyze_invalid_mode():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    with pytest.raises(RequestValidationError):
        client.analyze(bytecode="0xf00", analysis_mode="invalid")


def test_status():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    resp = client.status(uuid=testdata.UUID_1)

    assert type(resp) == respmodels.AnalysisStatusResponse
    assert_analysis(resp.analysis)


def test_running_analysis_not_ready():
    client = get_client([testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT])
    resp = client.analysis_ready(uuid=testdata.UUID_1)
    assert resp == False


def test_queued_analysis_not_ready():
    data = copy(testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT)
    data["status"] = "Queued"
    client = get_client([data])
    resp = client.analysis_ready(uuid=testdata.UUID_1)
    assert resp == False


def test_finished_analysis_ready():
    data = copy(testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT)
    data["status"] = "Finished"
    client = get_client([data])
    resp = client.analysis_ready(uuid=testdata.UUID_1)
    assert resp == True


def test_error_analysis_ready():
    data = copy(testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT)
    data["status"] = "Error"
    client = get_client([data])
    resp = client.analysis_ready(uuid=testdata.UUID_1)
    assert resp == True


def test_report():
    client = get_client([testdata.DETECTED_ISSUES_RESPONSE_DICT])
    resp = client.report(uuid=testdata.UUID_1)
    assert type(resp) == respmodels.DetectedIssuesResponse
    assert resp.source_type == testdata.SOURCE_TYPE
    assert resp.source_format == testdata.SOURCE_FORMAT
    assert resp.source_list == testdata.SOURCE_LIST
    assert resp.meta_data == {}
    assert len(resp.issues) == 1
    issue = resp.issues[0]
    assert issue.swc_id == testdata.SWC_ID
    assert issue.swc_title == testdata.SWC_TITLE
    assert issue.description_short == testdata.DESCRIPTION_HEAD
    assert issue.description_long == testdata.DESCRIPTION_TAIL
    assert issue.severity == testdata.SEVERITY
    assert issue.extra_data == {}
    assert len(issue.locations) == 1
    location = issue.locations[0]
    assert location.source_map == testdata.SOURCE_MAP
    assert location.source_type == testdata.SOURCE_TYPE
    assert location.source_format == testdata.SOURCE_FORMAT
    assert location.source_list == testdata.SOURCE_LIST


def test_openapi():
    client = get_client([testdata.OPENAPI_RESPONSE])
    resp = client.openapi()
    assert type(resp) == respmodels.OASResponse
    # we have to wrap this into quotes here because
    # of the test handler - content stays the same.
    assert resp.data == '"{}"'.format(testdata.OPENAPI_RESPONSE)


def test_version():
    client = get_client([testdata.VERSION_RESPONSE_DICT])
    resp = client.version()
    assert type(resp) == respmodels.VersionResponse
    assert resp.api_version == testdata.API_VERSION_1
    assert resp.maru_version == testdata.MARU_VERSION_1
    assert resp.mythril_version == testdata.MYTHRIL_VERSION_1
    assert resp.harvey_version == testdata.HARVEY_VERSION_1
    assert resp.hashed_version == testdata.HASHED_VERSION_1


def test_jwt_expiration():
    assert Client._get_jwt_expiration_ts(testdata.ACCESS_TOKEN_1) == datetime(
        2019, 2, 24, 16, 31, 19, 28000
    )
    assert Client._get_jwt_expiration_ts(testdata.REFRESH_TOKEN_1) == datetime(
        2019, 3, 24, 16, 21, 19, 28000
    )


def test_context_handler():
    with get_client([testdata.LOGOUT_RESPONSE_DICT]) as c:
        assert c is not None
