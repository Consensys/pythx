import json

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import AuthRefreshResponse

from . import common as testdata

ACCESS_TOKEN = "my_fancy_access_token"
REFRESH_TOKEN = "my_fancy_refresh_token"
AUTH_REFRESH = {"access": ACCESS_TOKEN, "refresh": REFRESH_TOKEN}
AUTH_REFRESH_RESPONSE = AuthRefreshResponse(
    access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN
)


def assert_auth_refresh_response(resp: AuthRefreshResponse):
    assert resp.access_token == testdata.ACCESS_TOKEN_1
    assert resp.refresh_token == testdata.REFRESH_TOKEN_1


def test_auth_refresh_response_from_valid_json():
    resp = AuthRefreshResponse.from_json(json.dumps(testdata.REFRESH_RESPONSE_DICT))
    assert_auth_refresh_response(resp)


def test_auth_refresh_response_from_invalid_json():
    with pytest.raises(ResponseValidationError):
        AuthRefreshResponse.from_json("{}")


def test_auth_refresh_response_from_valid_dict():
    resp = AuthRefreshResponse.from_dict(testdata.REFRESH_RESPONSE_DICT)
    assert_auth_refresh_response(resp)


def test_auth_refresh_response_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        AuthRefreshResponse.from_dict({})


def test_auth_refresh_response_to_json():
    assert (
        json.loads(testdata.REFRESH_RESPONSE_OBJECT.to_json())
        == testdata.REFRESH_RESPONSE_DICT
    )


def test_auth_refresh_response_to_dict():
    assert testdata.REFRESH_RESPONSE_OBJECT.to_dict() == testdata.REFRESH_RESPONSE_DICT
