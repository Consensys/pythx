import json

import pytest

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response import OASResponse

CONTENT = "openapi spec stuff"
OAS_RESPONSE = OASResponse(data=CONTENT)


def test_oas_response_from_valid_json():
    resp = OASResponse.from_json(CONTENT)
    assert resp.data == CONTENT


def test_oas_response_from_valid_dict():
    resp = OASResponse.from_dict({"data": CONTENT})
    assert resp.data == CONTENT


def test_oas_response_from_invalid_dict():
    with pytest.raises(ResponseDecodeError):
        OASResponse.from_dict({})


def test_oas_response_invalid_type():
    with pytest.raises(TypeError):
        OASResponse(data=1)


def test_oas_response_to_json():
    assert OAS_RESPONSE.to_json() == json.dumps({"data": CONTENT})


def test_oas_response_to_dict():
    assert OAS_RESPONSE.to_dict() == {"data": CONTENT}


def test_validate():
    OAS_RESPONSE.validate()
