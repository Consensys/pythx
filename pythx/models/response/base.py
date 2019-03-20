import abc
import json

import jsonschema

from pythx.models.exceptions import ResponseValidationError


class BaseResponse(abc.ABC):
    schema = None

    @classmethod
    def validate(cls, candidate):
        try:
            jsonschema.validate(candidate, cls.schema)
        except jsonschema.ValidationError as e:
            raise ResponseValidationError(e)

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @abc.abstractclassmethod
    def from_dict(cls, d: dict):
        pass

    def to_json(self):
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        pass
