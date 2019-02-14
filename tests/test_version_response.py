import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import VersionResponse


API_VERSION = "1.0"
MARU_VERSION = "1.1"
MYTHRIL_VERSION = "1.2"
HARVEY_VERSION = "1.3"
HASHED_VERSION = "31337deadbeef"

VERSION = {
    "api": API_VERSION,
    "maru": MARU_VERSION,
    "mythril": MYTHRIL_VERSION,
    "harvey": HARVEY_VERSION,
    "hash": HASHED_VERSION,
}

VERSION_REQUEST = VersionResponse(
    api_version=API_VERSION,
    maru_version=MARU_VERSION,
    mythril_version=MYTHRIL_VERSION,
    harvey_version=HARVEY_VERSION,
    hashed_version=HASHED_VERSION,
)


def assert_version_response(resp: VersionResponse):
    assert resp.api_version == API_VERSION
    assert resp.maru_version == MARU_VERSION
    assert resp.mythril_version == MYTHRIL_VERSION
    assert resp.harvey_version == HARVEY_VERSION
    assert resp.hashed_version == HASHED_VERSION


def test_auth_logout_request_from_valid_json():
    resp = VersionResponse.from_json(json.dumps(VERSION))
    assert_version_response(resp)


def test_auth_logout_request_from_valid_dict():
    resp = VersionResponse.from_dict(VERSION)
    assert_version_response(resp)


def test_auth_logout_request_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        VersionResponse.from_dict({})


def test_auth_logout_request_from_invalid_json():
    with pytest.raises(ResponseDecodeError):
        VersionResponse.from_json("{}")


def test_auth_logout_request_to_json():
    assert json.loads(VERSION_REQUEST.to_json()) == VERSION


def test_auth_logout_request_to_dict():
    assert VERSION_REQUEST.to_dict() == VERSION


def test_validate():
    VERSION_REQUEST.validate()
