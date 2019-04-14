import pytest

from pythx.middleware.analysiscache import AnalysisCacheMiddleware
from pythx.middleware.toolname import ClientToolNameMiddleware

from . import common as testdata

FALSE_CACHE_MIDDLEWARE = AnalysisCacheMiddleware(no_cache=False)
TRUE_CACHE_MIDDLEWARE = AnalysisCacheMiddleware(no_cache=True)


@pytest.mark.parametrize(
    "middleware,request_dict,flag_added,lookup_value",
    [
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            True,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            TRUE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            True,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FALSE_CACHE_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            False,
        ),
    ],
)
def test_request_dicts(middleware, request_dict, flag_added, lookup_value):
    new_request = middleware.process_request(request_dict)
    if flag_added:
        assert new_request["payload"].get("noCacheLookup") == lookup_value
        del new_request["payload"]["noCacheLookup"]

    # rest of the result should stay the same
    assert request_dict == new_request


@pytest.mark.parametrize(
    "middleware,resp_obj",
    [
        (FALSE_CACHE_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (FALSE_CACHE_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (TRUE_CACHE_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
    ],
)
def test_response_models(middleware, resp_obj):
    new_resp_obj = middleware.process_response(resp_obj)
    assert new_resp_obj == resp_obj
