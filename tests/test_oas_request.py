import json

import pytest

from pythx.models.exceptions import RequestDecodeError
from pythx.models.request import OASRequest


OAS_REQUEST = OASRequest(mode="yaml")


def assert_version_request(req):
    assert req.method == "GET"
    assert req.headers == {}
    assert req.parameters == {}
    assert req.payload == {}
    if req.mode == "html":
        assert req.endpoint == "v1/openapi"
    else:
        assert req.endpoint == "v1/openapi.yaml"


def test_oas_request_from_valid_json():
    req = OASRequest.from_json("{}")
    assert_version_request(req)


def test_oas_request_from_valid_dict():
    req = OASRequest.from_dict({})
    assert_version_request(req)


def test_invalid_format():
    with pytest.raises(RequestDecodeError):
        OASRequest(mode="invalid")


def test_oas_request_to_json():
    assert OAS_REQUEST.to_json() == "{}"


def test_oas_request_to_dict():
    assert OAS_REQUEST.to_dict() == {}


def test_validate():
    OAS_REQUEST.validate()
