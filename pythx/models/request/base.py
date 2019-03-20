import abc
import json
import jsonschema
from pythx.models.exceptions import RequestValidationError


class BaseRequest(abc.ABC):
    schema = None

    @classmethod
    def validate(cls, candidate):
        try:
            jsonschema.validate(candidate, cls.schema)
        except jsonschema.ValidationError as e:
            raise RequestValidationError(e)

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

    @abc.abstractproperty
    def payload(self):
        pass

    @abc.abstractproperty
    def headers(self):
        pass

    @abc.abstractproperty
    def parameters(self):
        pass

    @abc.abstractproperty
    def method(self):
        pass
