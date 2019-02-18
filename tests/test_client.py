import json
from copy import copy
from datetime import datetime

import pytest

import pythx.models.response as respmodels
from pythx.api import APIHandler, Client
from pythx.models.exceptions import PythXAPIError, RequestValidationError
from pythx.models.response.analysis import AnalysisStatus
from pythx.models.util import serialize_api_timestamp


class MockAPIHandler(APIHandler):
    def __init__(self, resp):
        super().__init__()
        self.resp = resp

    def send_request(self, *args, **kwargs):
        return json.dumps(self.resp.pop(0))


API_VERSION = "1.0"
MARU_VERSION = "1.1"
MYTHRIL_VERSION = "1.2"
HARVEY_VERSION = "1.3"
HASHED_VERSION = "31337deadbeef"
DEFAULT_ACCESS_TOKEN = "my_default_access_token"
DEFAULT_REFRESH_TOKEN = "my_default_refresh_token"
ACCESS_TOKEN = "my_fancy_access_token"
REFRESH_TOKEN = "my_fancy_refresh_token"
AUTH_DATE = datetime.now()
API_LOGIN_RESPONSE = {"access": ACCESS_TOKEN, "refresh": REFRESH_TOKEN}
API_LOGOUT_RESPONSE = {}
API_REFRESH_RESPONSE = API_LOGIN_RESPONSE
OPENAPI_RESPONSE = "openapi"
VERSION_RESPONSE = {
    "api": API_VERSION,
    "maru": MARU_VERSION,
    "mythril": MYTHRIL_VERSION,
    "harvey": HARVEY_VERSION,
    "hash": HASHED_VERSION,
}
UUID_1 = "0680a1e2-b908-4c9a-a15b-636ef9b61486"
API_VERSION_1 = "v1.3.0"
MARU_VERSION_1 = "v0.2.0"
MYTHRIL_VERSION_1 = "0.19.11"
QUEUE_TIME_1 = 1
RUN_TIME_1 = 300
STATUS_1 = "Running"
SUBMITTED_AT_1 = "2019-01-10T01:29:38.410Z"
SUBMITTED_BY_1 = "000008544b0aa00010a91111"
API_SUBMISSION_RESPONSE = {
    "uuid": UUID_1,
    "apiVersion": API_VERSION_1,
    "maruVersion": MARU_VERSION_1,
    "mythrilVersion": MYTHRIL_VERSION_1,
    "queueTime": QUEUE_TIME_1,
    "runTime": RUN_TIME_1,
    "status": STATUS_1,
    "submittedAt": SUBMITTED_AT_1,
    "submittedBy": SUBMITTED_BY_1,
}
API_LIST_RESPONSE = {
    "analyses": [
        {
            "uuid": UUID_1,
            "apiVersion": API_VERSION_1,
            "maruVersion": MARU_VERSION_1,
            "mythrilVersion": MYTHRIL_VERSION_1,
            "queueTime": QUEUE_TIME_1,
            "runTime": RUN_TIME_1,
            "status": STATUS_1,
            "submittedAt": SUBMITTED_AT_1,
            "submittedBy": SUBMITTED_BY_1,
        },
        {
            "uuid": UUID_1,
            "apiVersion": API_VERSION_1,
            "maruVersion": MARU_VERSION_1,
            "mythrilVersion": MYTHRIL_VERSION_1,
            "queueTime": QUEUE_TIME_1,
            "runTime": RUN_TIME_1,
            "status": STATUS_1,
            "submittedAt": SUBMITTED_AT_1,
            "submittedBy": SUBMITTED_BY_1,
        },
    ],
    "total": 2,
}
SWC_ID = "SWC-103"
SWC_TITLE = "Floating Pragma"
DESCRIPTION_HEAD = "A floating pragma is set."
DESCRIPTION_TAIL = 'It is recommended to make a conscious choice on what version of Solidity is used for compilation. Currently any version equal or greater than \\"0.4.24\\" is allowed.'
SEVERITY = "Low"
SOURCE_MAP = "48:1:0"
SOURCE_TYPE = "raw-bytecode"
SOURCE_FORMAT = "evm-byzantium-bytecode"
SOURCE_LIST = "/test/my-super-safe-contract.sol"
VALID_ISSUES = [
    {
        "issues": [
            {
                "swcID": SWC_ID,
                "swcTitle": SWC_TITLE,
                "description": {"head": DESCRIPTION_HEAD, "tail": DESCRIPTION_TAIL},
                "severity": SEVERITY,
                "locations": [
                    {
                        "sourceMap": SOURCE_MAP,
                        "sourceType": SOURCE_TYPE,
                        "sourceFormat": SOURCE_FORMAT,
                        "sourceList": [SOURCE_LIST],
                    }
                ],
                "extra": {},
            }
        ],
        "sourceType": SOURCE_TYPE,
        "sourceFormat": SOURCE_FORMAT,
        "sourceList": [SOURCE_LIST],
        "meta": {},
    }
]


def get_client(resp_data, logged_in=True):
    client = Client(
        eth_address="0xdeadbeef",
        password="supersecure",
        handler=MockAPIHandler(resp_data),
    )
    if logged_in:
        # simulate that we're already logged in
        client.access_token = DEFAULT_ACCESS_TOKEN
        client.refresh_token = DEFAULT_REFRESH_TOKEN
        client.last_auth_ts = AUTH_DATE
    return client


def test_login():
    client = get_client([API_LOGIN_RESPONSE], logged_in=False)

    assert client.access_token is None
    assert client.refresh_token is None
    assert client.last_auth_ts is None

    resp = client.login()

    assert type(resp) == respmodels.AuthLoginResponse
    assert resp.access_token == ACCESS_TOKEN
    assert resp.refresh_token == REFRESH_TOKEN

    assert client.access_token == ACCESS_TOKEN
    assert client.refresh_token == REFRESH_TOKEN
    assert type(client.last_auth_ts) == datetime


def test_logout():
    client = get_client([API_LOGOUT_RESPONSE])
    resp = client.logout()

    assert type(resp) == respmodels.AuthLogoutResponse
    assert client.access_token is None
    assert client.refresh_token is None
    assert client.last_auth_ts is None


def test_refresh():
    client = get_client([API_REFRESH_RESPONSE])
    resp = client.refresh()

    assert type(resp) == respmodels.AuthRefreshResponse
    assert resp.access_token == ACCESS_TOKEN
    assert resp.refresh_token == REFRESH_TOKEN
    assert resp.to_dict() == API_REFRESH_RESPONSE

    assert type(client.last_auth_ts) == datetime
    assert client.last_auth_ts != AUTH_DATE
    assert client.access_token == ACCESS_TOKEN
    assert client.refresh_token == REFRESH_TOKEN


def test_analysis_list():
    client = get_client([API_LIST_RESPONSE])
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )

    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(API_LIST_RESPONSE["analyses"])
    assert resp.to_dict() == API_LIST_RESPONSE


def test_auto_login():
    client = get_client([API_LOGIN_RESPONSE, API_LIST_RESPONSE], logged_in=False)
    resp = client.analysis_list(
        date_from=datetime(2018, 1, 1), date_to=datetime(2019, 1, 1)
    )
    assert type(resp) == respmodels.AnalysisListResponse
    assert resp.total == len(API_LIST_RESPONSE["analyses"])
    assert resp.to_dict() == API_LIST_RESPONSE


def assert_analysis(analysis):
    assert analysis.uuid == UUID_1
    assert analysis.api_version == API_VERSION_1
    assert analysis.mythril_version == MYTHRIL_VERSION_1
    assert analysis.maru_version == MARU_VERSION_1
    assert analysis.run_time == RUN_TIME_1
    assert analysis.queue_time == QUEUE_TIME_1
    assert analysis.status == AnalysisStatus(STATUS_1)
    assert serialize_api_timestamp(analysis.submitted_at) == SUBMITTED_AT_1
    assert analysis.submitted_by == SUBMITTED_BY_1


def test_analyze_bytecode():
    client = get_client([API_SUBMISSION_RESPONSE])
    resp = client.analyze(bytecode="0xf00")

    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_source_code():
    client = get_client([API_SUBMISSION_RESPONSE])
    resp = client.analyze(sources={"foo.sol": "bar"})

    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_source_and_bytecode():
    client = get_client([API_SUBMISSION_RESPONSE])
    resp = client.analyze(sources={"foo.sol": "bar"}, bytecode="0xf00")
    assert type(resp) == respmodels.AnalysisSubmissionResponse
    assert_analysis(resp.analysis)


def test_analyze_missing_data():
    client = get_client([API_SUBMISSION_RESPONSE])
    with pytest.raises(RequestValidationError):
        client.analyze()


def test_analyze_invalid_mode():
    client = get_client([API_SUBMISSION_RESPONSE])
    with pytest.raises(RequestValidationError):
        client.analyze(bytecode="0xf00", analysis_mode="invalid")


def test_status():
    client = get_client([API_SUBMISSION_RESPONSE])
    resp = client.status(uuid=UUID_1)

    assert type(resp) == respmodels.AnalysisStatusResponse
    assert_analysis(resp.analysis)


def test_running_analysis_not_ready():
    client = get_client([API_SUBMISSION_RESPONSE])
    resp = client.analysis_ready(uuid=UUID_1)
    assert resp == False


def test_queued_analysis_not_ready():
    data = copy(API_SUBMISSION_RESPONSE)
    data["status"] = "Queued"
    client = get_client([data])
    resp = client.analysis_ready(uuid=UUID_1)
    assert resp == False


def test_finished_analysis_ready():
    data = copy(API_SUBMISSION_RESPONSE)
    data["status"] = "Finished"
    client = get_client([data])
    resp = client.analysis_ready(uuid=UUID_1)
    assert resp == True


def test_error_analysis_ready():
    data = copy(API_SUBMISSION_RESPONSE)
    data["status"] = "Error"
    client = get_client([data])
    resp = client.analysis_ready(uuid=UUID_1)
    assert resp == True


def test_report():
    client = get_client([VALID_ISSUES])
    resp = client.report(uuid=UUID_1)
    assert type(resp) == respmodels.DetectedIssuesResponse
    assert resp.source_type == SOURCE_TYPE
    assert resp.source_format == SOURCE_FORMAT
    assert resp.source_list == [SOURCE_LIST]
    assert resp.meta_data == {}
    assert len(resp.issues) == 1
    issue = resp.issues[0]
    assert issue.swc_id == SWC_ID
    assert issue.swc_title == SWC_TITLE
    assert issue.description_short == DESCRIPTION_HEAD
    assert issue.description_long == DESCRIPTION_TAIL
    assert issue.severity == SEVERITY
    assert issue.extra_data == {}
    assert len(issue.locations) == 1
    location = issue.locations[0]
    assert location.source_map == SOURCE_MAP
    assert location.source_type == SOURCE_TYPE
    assert location.source_format == SOURCE_FORMAT
    assert location.source_list == [SOURCE_LIST]


def test_openapi():
    client = get_client([OPENAPI_RESPONSE])
    resp = client.openapi()
    assert type(resp) == respmodels.OASResponse
    # we have to wrap this into quotes here because
    # of the test handler - content stays the same.
    assert resp.data == '"{}"'.format(OPENAPI_RESPONSE)


def test_version():
    client = get_client([VERSION_RESPONSE])
    resp = client.version()
    assert type(resp) == respmodels.VersionResponse
    assert resp.api_version == API_VERSION
    assert resp.maru_version == MARU_VERSION
    assert resp.mythril_version == MYTHRIL_VERSION
    assert resp.harvey_version == HARVEY_VERSION
    assert resp.hashed_version == HASHED_VERSION
