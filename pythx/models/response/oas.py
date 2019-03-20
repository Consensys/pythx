from typing import Dict

from pythx.models.exceptions import ResponseDecodeError
from pythx.models.response.base import BaseResponse


class OASResponse(BaseResponse):
    def __init__(self, data: str):
        if not type(data) == str:
            raise TypeError("Expected data type str but got {}".format(type(data)))
        self.data = data

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d: Dict):
        if not "data" in d:
            raise ResponseDecodeError("Expected 'data' field but got {}".format(d))
        return cls(data=d["data"])

    @classmethod
    def from_json(cls, json_str: str):
        # overwrite from base response because the API doesn't actually deliver
        # JSON but raw YAML/HTML
        return cls.from_dict({"data": json_str})

    def to_dict(self):
        return {"data": self.data}
