import json

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import VersionResponse

from . import common as testdata


def assert_version_response(resp: VersionResponse):
    assert resp.api_version == testdata.API_VERSION_1
    assert resp.maru_version == testdata.MARU_VERSION_1
    assert resp.mythril_version == testdata.MYTHRIL_VERSION_1
    assert resp.maestro_version == testdata.MAESTRO_VERSION_1
    assert resp.harvey_version == testdata.HARVEY_VERSION_1
    assert resp.hashed_version == testdata.HASHED_VERSION_1


def test_auth_logout_request_from_valid_json():
    resp = VersionResponse.from_json(json.dumps(testdata.VERSION_RESPONSE_DICT))
    assert_version_response(resp)


def test_auth_logout_request_from_valid_dict():
    resp = VersionResponse.from_dict(testdata.VERSION_RESPONSE_DICT)
    assert_version_response(resp)


def test_auth_logout_request_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        VersionResponse.from_dict({})


def test_auth_logout_request_from_invalid_json():
    with pytest.raises(ResponseValidationError):
        VersionResponse.from_json("{}")


def test_auth_logout_request_to_json():
    assert (
        json.loads(testdata.VERSION_RESPONSE_OBJECT.to_json())
        == testdata.VERSION_RESPONSE_DICT
    )


def test_auth_logout_request_to_dict():
    assert testdata.VERSION_RESPONSE_OBJECT.to_dict() == testdata.VERSION_RESPONSE_DICT
