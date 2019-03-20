import pytest

from . import common as testdata
from pythx.middleware.toolname import ClientToolNameMiddleware


DEFAULT_CTN_MIDDLEWARE = ClientToolNameMiddleware()
CUSTOM_CTN_MIDDLEWARE = ClientToolNameMiddleware(name="test")


def generate_request_dict(req):
    return {
        "method": req.method,
        "payload": req.payload,
        "params": req.parameters,
        "headers": req.headers,
        "url": "https://test.com/" + req.endpoint,
    }


@pytest.mark.parametrize(
    "middleware,request_dict,name_added",
    [
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT), False),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT), False),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT), False),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT), True),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.LOGIN_REQUEST_OBJECT), False),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT), False),
        (DEFAULT_CTN_MIDDLEWARE, generate_request_dict(testdata.REFRESH_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT), True),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.LOGIN_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT), False),
        (CUSTOM_CTN_MIDDLEWARE, generate_request_dict(testdata.REFRESH_REQUEST_OBJECT), False),
    ],
)
def test_request_dicts(middleware, request_dict, name_added):
    new_request = middleware.process_request(request_dict)
    if name_added:
        assert new_request["payload"].get("clientToolName") == middleware.name
        del new_request["payload"]["clientToolName"]

    # rest of the result should stay the same
    assert request_dict == new_request


@pytest.mark.parametrize(
    "middleware,resp_obj",
    [
        (DEFAULT_CTN_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (DEFAULT_CTN_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (CUSTOM_CTN_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
    ],
)
def test_response_models(middleware, resp_obj):
    new_resp_obj = middleware.process_response(resp_obj)
    assert new_resp_obj == resp_obj
