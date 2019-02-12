import json

import pytest

from pythx.core.exceptions import RequestDecodeError
from pythx.core.request.models import AuthLoginRequest

ETH_ADDRESS = "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"
PASSWORD = "supersecure"
USER_ID = "31337"

LOGIN = {"ethAddress": ETH_ADDRESS, "password": PASSWORD, "userId": USER_ID}
LOGIN_REQUEST = AuthLoginRequest(
    eth_address=ETH_ADDRESS, password=PASSWORD, user_id=USER_ID
)


def assert_login_request(req: AuthLoginRequest):
    assert req.eth_address == ETH_ADDRESS
    assert req.password == PASSWORD
    assert req.user_id == USER_ID


def test_auth_login_request_from_valid_json():
    req = AuthLoginRequest.from_json(json.dumps(LOGIN))
    assert_login_request(req)


def test_auth_login_request_from_invalid_json():
    with pytest.raises(RequestDecodeError):
        AuthLoginRequest.from_json("{}")


def test_auth_login_request_from_valid_dict():
    req = AuthLoginRequest.from_dict(LOGIN)
    assert_login_request(req)


def test_auth_login_request_from_invalid_dict():
    with pytest.raises(RequestDecodeError):
        AuthLoginRequest.from_dict({})


def test_auth_login_request_to_json():
    assert json.loads(LOGIN_REQUEST.to_json()) == LOGIN


def test_auth_login_request_to_dict():
    assert LOGIN_REQUEST.to_dict() == LOGIN
