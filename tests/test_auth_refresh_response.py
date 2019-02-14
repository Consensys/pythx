import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import AuthRefreshResponse

ACCESS_TOKEN = "my_fancy_access_token"
REFRESH_TOKEN = "my_fancy_refresh_token"
AUTH_REFRESH = {"access": ACCESS_TOKEN, "refresh": REFRESH_TOKEN}
AUTH_REFRESH_RESPONSE = AuthRefreshResponse(
    access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN
)


def assert_auth_refresh_response(resp: AuthRefreshResponse):
    assert resp.access_token == ACCESS_TOKEN
    assert resp.refresh_token == REFRESH_TOKEN


def test_auth_refresh_response_from_valid_json():
    resp = AuthRefreshResponse.from_json(json.dumps(AUTH_REFRESH))
    assert_auth_refresh_response(resp)


def test_auth_refresh_response_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AuthRefreshResponse.from_json("{}")


def test_auth_refresh_response_from_valid_dict():
    resp = AuthRefreshResponse.from_dict(AUTH_REFRESH)
    assert_auth_refresh_response(resp)


def test_auth_refresh_response_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        AuthRefreshResponse.from_dict({})


def test_auth_refresh_response_to_json():
    assert json.loads(AUTH_REFRESH_RESPONSE.to_json()) == AUTH_REFRESH


def test_auth_refresh_response_to_dict():
    assert AUTH_REFRESH_RESPONSE.to_dict() == AUTH_REFRESH


def test_validate():
    AUTH_REFRESH_RESPONSE.validate()
