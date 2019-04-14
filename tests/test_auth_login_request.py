import json

import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AuthLoginRequest

from . import common as testdata


def assert_login(req: AuthLoginRequest):
    assert req.eth_address == testdata.ETH_ADDRESS
    assert req.password == testdata.PASSWORD
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == testdata.LOGIN_REQUEST_DICT


def test_login_from_valid_json():
    req = AuthLoginRequest.from_json(json.dumps(testdata.LOGIN_REQUEST_DICT))
    assert_login(req)


def test_login_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AuthLoginRequest.from_json("{}")


def test_login_from_valid_dict():
    req = AuthLoginRequest.from_dict(testdata.LOGIN_REQUEST_DICT)
    assert_login(req)


def test_login_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AuthLoginRequest.from_dict({})


def test_login_to_json():
    assert (
        json.loads(testdata.LOGIN_REQUEST_OBJECT.to_json())
        == testdata.LOGIN_REQUEST_DICT
    )


def test_login_to_dict():
    assert testdata.LOGIN_REQUEST_OBJECT.to_dict() == testdata.LOGIN_REQUEST_DICT
