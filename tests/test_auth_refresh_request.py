import json

import pytest

from pythx.models.exceptions import RequestValidationError
from pythx.models.request import AuthRefreshRequest

from . import common as testdata


def assert_auth_refresh_request(req: AuthRefreshRequest):
    assert req.access_token == testdata.ACCESS_TOKEN_1
    assert req.refresh_token == testdata.REFRESH_TOKEN_1
    assert req.method == "POST"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == testdata.REFRESH_REQUEST_PAYLOAD_DICT


def test_auth_refresh_request_from_valid_json():
    resp = AuthRefreshRequest.from_json(json.dumps(testdata.REFRESH_REQUEST_DICT))
    assert_auth_refresh_request(resp)


def test_auth_refresh_request_from_invalid_json():
    with pytest.raises(RequestValidationError):
        AuthRefreshRequest.from_json("{}")


def test_auth_refresh_request_from_valid_dict():
    resp = AuthRefreshRequest.from_dict(testdata.REFRESH_REQUEST_DICT)
    assert_auth_refresh_request(resp)


def test_auth_refresh_request_from_invalid_dict():
    with pytest.raises(RequestValidationError):
        AuthRefreshRequest.from_dict({})


def test_auth_refresh_request_to_json():
    assert (
        json.loads(testdata.REFRESH_REQUEST_OBJECT.to_json())
        == testdata.REFRESH_REQUEST_DICT
    )


def test_auth_refresh_request_to_dict():
    assert testdata.REFRESH_REQUEST_OBJECT.to_dict() == testdata.REFRESH_REQUEST_DICT
