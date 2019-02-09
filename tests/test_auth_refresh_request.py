from pythx.core.request.models import AuthRefreshRequest
from pythx.core.exceptions import RequestDecodeError
import json
import pytest


ACCESS_TOKEN = "my_fancy_access_token"
REFRESH_TOKEN = "my_fancy_refresh_token"
AUTH_REFRESH = {"access": ACCESS_TOKEN, "refresh": REFRESH_TOKEN}
AUTH_REFRESH_REQUEST = AuthRefreshRequest(
    access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN
)


def assert_auth_refresh_request(resp: AuthRefreshRequest):
    assert resp.access_token == ACCESS_TOKEN
    assert resp.refresh_token == REFRESH_TOKEN


def test_auth_refresh_request_from_valid_json():
    resp = AuthRefreshRequest.from_json(json.dumps(AUTH_REFRESH))
    assert_auth_refresh_request(resp)


def test_auth_refresh_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AuthRefreshRequest.from_json("{}")


def test_auth_refresh_request_from_valid_dict():
    resp = AuthRefreshRequest.from_dict(AUTH_REFRESH)
    assert_auth_refresh_request(resp)


def test_auth_refresh_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AuthRefreshRequest.from_dict({})


def test_auth_refresh_request_to_json():
    assert json.loads(AUTH_REFRESH_REQUEST.to_json()) == AUTH_REFRESH


def test_auth_refresh_request_to_dict():
    assert AUTH_REFRESH_REQUEST.to_dict() == AUTH_REFRESH
