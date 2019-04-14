import json

import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AuthLogoutRequest

from . import common as testdata


def assert_logout_request(req):
    assert req.global_ == testdata.GLOBAL_LOGOUT
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}


def test_auth_logout_request_from_valid_json():
    req = AuthLogoutRequest.from_json(json.dumps(testdata.LOGOUT_REQUEST_DICT))
    assert_logout_request(req)


def test_auth_logout_request_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AuthLogoutRequest.from_json("{}")


def test_auth_logout_request_from_valid_dict():
    req = AuthLogoutRequest.from_dict(testdata.LOGOUT_REQUEST_DICT)
    assert_logout_request(req)


def test_auth_logout_request_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AuthLogoutRequest.from_dict({})


def test_auth_logout_request_to_json():
    assert (
        json.loads(testdata.LOGOUT_REQUEST_OBJECT.to_json())
        == testdata.LOGOUT_REQUEST_DICT
    )


def test_auth_logout_request_to_dict():
    assert testdata.LOGOUT_REQUEST_OBJECT.to_dict() == testdata.LOGOUT_REQUEST_DICT
