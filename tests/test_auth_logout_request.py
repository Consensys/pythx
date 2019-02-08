import json

import pytest

from pythx.core.exceptions import RequestDecodeError
from pythx.core.request.models import AuthLogoutRequest


GLOBAL = True

LOGOUT = {"global": GLOBAL}
LOGOUT_REQUEST = AuthLogoutRequest(global_=GLOBAL)


def test_auth_logout_request_from_valid_json():
    req = AuthLogoutRequest.from_json(json.dumps(LOGOUT))
    assert req.global_ == GLOBAL


def test_auth_logout_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AuthLogoutRequest.from_json("{}")


def test_auth_logout_request_from_valid_dict():
    req = AuthLogoutRequest.from_dict(LOGOUT)
    assert req.global_ == GLOBAL


def test_auth_logout_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AuthLogoutRequest.from_dict({})


def test_auth_logout_request_to_json():
    assert json.loads(LOGOUT_REQUEST.to_json()) == LOGOUT


def test_auth_logout_request_to_dict():
    assert LOGOUT_REQUEST.to_dict() == LOGOUT
