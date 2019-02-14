import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import AuthLogoutResponse

AUTH_LOGOUT_RESPONSE = AuthLogoutResponse()


def test_auth_login_response_from_valid_json():
    resp = AuthLogoutResponse.from_json("{}")
    assert type(resp) == AuthLogoutResponse

def test_auth_login_response_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AuthLogoutResponse.from_json('{"foo": "bar"}')


def test_auth_login_response_from_valid_dict():
    resp = AuthLogoutResponse.from_dict({})
    assert type(resp) == AuthLogoutResponse

def test_auth_login_response_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        AuthLogoutResponse.from_dict({"foo": "bar"})


def test_auth_login_response_to_json():
    assert AUTH_LOGOUT_RESPONSE.to_json() == "{}"


def test_auth_login_response_to_dict():
    assert AUTH_LOGOUT_RESPONSE.to_dict() == {}


def test_validate():
    AUTH_LOGOUT_RESPONSE.validate()
