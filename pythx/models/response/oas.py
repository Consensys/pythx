import json
from typing import Dict

from pythx.models.response.base import BaseResponse
from pythx.models.util import resolve_schema


class OASResponse(BaseResponse):
    with open(resolve_schema(__file__, "openapi.json")) as sf:
        schema = json.load(sf)

    def __init__(self, data: str):
        if not type(data) == str:
            raise TypeError("Expected data type str but got {}".format(type(data)))
        self.data = data

    @classmethod
    def from_dict(cls, d: Dict):
        cls.validate(d)
        return cls(data=d["data"])

    @classmethod
    def from_json(cls, json_str: str):
        # overwrite from base response because the API doesn't actually deliver
        # JSON but raw YAML/HTML
        return cls.from_dict({"data": json_str})

    def to_dict(self):
        d = {"data": self.data}
        return d
