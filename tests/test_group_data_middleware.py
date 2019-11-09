import pytest

from pythx.middleware.group_data import GroupDataMiddleware

from . import common as testdata

EMPTY_MIDDLEWARE = GroupDataMiddleware()
ID_ONLY_MIDDLEWARE = GroupDataMiddleware(group_id="test-id")
NAME_ONLY_MIDDLEWARE = GroupDataMiddleware(group_name="test-name")
FULL_MIDDLEWARE = GroupDataMiddleware(group_id="test-id", group_name="test-name")


@pytest.mark.parametrize(
    "middleware,request_dict,id_added,name_added",
    [
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            EMPTY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            True,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            ID_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            False,
            True,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            NAME_ONLY_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_LIST_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.DETECTED_ISSUES_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_STATUS_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.ANALYSIS_SUBMISSION_REQUEST_OBJECT),
            True,
            True,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGIN_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.LOGOUT_REQUEST_OBJECT),
            False,
            False,
        ),
        (
            FULL_MIDDLEWARE,
            testdata.generate_request_dict(testdata.REFRESH_REQUEST_OBJECT),
            False,
            False,
        ),
    ],
)
def test_request_dicts(middleware, request_dict, id_added, name_added):
    new_request = middleware.process_request(request_dict)
    if id_added:
        assert new_request["payload"].get("groupId") == middleware.group_id
        del new_request["payload"]["groupId"]
    if name_added:
        assert new_request["payload"].get("groupName") == middleware.group_name
        del new_request["payload"]["groupName"]

    # rest of the result should stay the same
    assert request_dict == new_request


@pytest.mark.parametrize(
    "middleware,resp_obj",
    [
        (EMPTY_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (EMPTY_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (ID_ONLY_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (NAME_ONLY_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.ANALYSIS_LIST_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.DETECTED_ISSUES_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.ANALYSIS_STATUS_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.ANALYSIS_SUBMISSION_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.LOGIN_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.LOGOUT_RESPONSE_OBJECT),
        (FULL_MIDDLEWARE, testdata.REFRESH_RESPONSE_OBJECT),
    ],
)
def test_response_models(middleware, resp_obj):
    new_resp_obj = middleware.process_response(resp_obj)
    assert new_resp_obj == resp_obj
