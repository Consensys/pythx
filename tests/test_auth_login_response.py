from pythx.core.response.models import AuthLoginResponse
from pythx.core.exceptions import ResponseDecodeError
import json
import pytest


ACCESS_TOKEN = "my_fancy_access_token"
REFRESH_TOKEN = "my_fancy_refresh_token"
AUTH_LOGIN = {"accessToken": ACCESS_TOKEN, "refreshToken": REFRESH_TOKEN}
AUTH_LOGIN_RESPONSE = AuthLoginResponse(
    access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN
)


def assert_auth_login_response(resp: AuthLoginResponse):
    assert resp.access_token == ACCESS_TOKEN
    assert resp.refresh_token == REFRESH_TOKEN


def test_auth_login_response_from_valid_json():
    resp = AuthLoginResponse.from_json(json.dumps(AUTH_LOGIN))
    assert_auth_login_response(resp)


def test_auth_login_response_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AuthLoginResponse.from_json("{}")


def test_auth_login_response_from_valid_dict():
    resp = AuthLoginResponse.from_dict(AUTH_LOGIN)
    assert_auth_login_response(resp)


def test_auth_login_response_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        AuthLoginResponse.from_dict({})


def test_auth_login_response_to_json():
    assert json.loads(AUTH_LOGIN_RESPONSE.to_json()) == AUTH_LOGIN


def test_auth_login_response_to_dict():
    assert AUTH_LOGIN_RESPONSE.to_dict() == AUTH_LOGIN
