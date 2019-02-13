import json

import pytest

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import AuthLogoutRequest

GLOBAL = True

LOGOUT = {"global": GLOBAL}
LOGOUT_REQUEST = AuthLogoutRequest(global_=GLOBAL)


def assert_logout_request(req):
    assert req.global_ == GLOBAL
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}


def test_auth_logout_request_from_valid_json():
    req = AuthLogoutRequest.from_json(json.dumps(LOGOUT))
    assert_logout_request(req)


def test_auth_logout_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AuthLogoutRequest.from_json("{}")


def test_auth_logout_request_from_valid_dict():
    req = AuthLogoutRequest.from_dict(LOGOUT)
    assert_logout_request(req)


def test_auth_logout_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AuthLogoutRequest.from_dict({})


def test_auth_logout_request_to_json():
    assert json.loads(LOGOUT_REQUEST.to_json()) == LOGOUT


def test_auth_logout_request_to_dict():
    assert LOGOUT_REQUEST.to_dict() == LOGOUT
