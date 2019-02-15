import json

import pytest

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import VersionRequest

VERSION_REQUEST = VersionRequest()


def assert_version_request(req):
    assert req.method == "GET"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}
    assert req.endpoint == "v1/version"


def test_auth_logout_request_from_valid_json():
    req = VersionRequest.from_json("{}")
    assert_version_request(req)


def test_auth_logout_request_from_valid_dict():
    req = VersionRequest.from_dict({})
    assert_version_request(req)


def test_auth_logout_request_to_json():
    assert VERSION_REQUEST.to_json() == "{}"


def test_auth_logout_request_to_dict():
    assert VERSION_REQUEST.to_dict() == {}


def test_validate():
    VERSION_REQUEST.validate()
