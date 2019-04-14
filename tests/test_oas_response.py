import json

import pytest

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response import OASResponse

from . import common as testdata


def test_oas_response_from_valid_json():
    resp = OASResponse.from_json(testdata.OPENAPI_RESPONSE)
    assert resp.data == testdata.OPENAPI_RESPONSE


def test_oas_response_from_valid_dict():
    resp = OASResponse.from_dict({"data": testdata.OPENAPI_RESPONSE})
    assert resp.data == testdata.OPENAPI_RESPONSE


def test_oas_response_from_invalid_dict():
    with pytest.raises(ResponseValidationError):
        OASResponse.from_dict({})


def test_oas_response_invalid_type():
    with pytest.raises(TypeError):
        OASResponse(data=1)


def test_oas_response_to_json():
    assert testdata.OPENAPI_RESPONSE_OBJECT.to_json() == json.dumps(
        {"data": testdata.OPENAPI_RESPONSE}
    )


def test_oas_response_to_dict():
    assert testdata.OPENAPI_RESPONSE_OBJECT.to_dict() == {
        "data": testdata.OPENAPI_RESPONSE
    }
