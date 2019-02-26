import json

import pytest

from . import common as testdata
from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import AuthLoginResponse


def assert_auth_login_response(resp: AuthLoginResponse):
    assert resp.access_token == testdata.ACCESS_TOKEN_1
    assert resp.refresh_token == testdata.REFRESH_TOKEN_1


def test_auth_login_response_from_valid_json():
    resp = AuthLoginResponse.from_json(json.dumps(testdata.LOGIN_RESPONSE_DICT))
    assert_auth_login_response(resp)


def test_auth_login_response_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        AuthLoginResponse.from_json("{}")


def test_auth_login_response_from_valid_dict():
    resp = AuthLoginResponse.from_dict(testdata.LOGIN_RESPONSE_DICT)
    assert_auth_login_response(resp)


def test_auth_login_response_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        AuthLoginResponse.from_dict({})


def test_auth_login_response_to_json():
    assert (
        json.loads(testdata.LOGIN_RESPONSE_OBJECT.to_json())
        == testdata.LOGIN_RESPONSE_DICT
    )


def test_auth_login_response_to_dict():
    assert testdata.LOGIN_RESPONSE_OBJECT.to_dict() == testdata.LOGIN_RESPONSE_DICT


def test_validate():
    testdata.LOGIN_RESPONSE_OBJECT.validate()
