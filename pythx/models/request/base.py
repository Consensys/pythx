import abc
import json


class BaseRequest(abc.ABC):
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

    # @abc.abstractmethod
    # def validate(self):
    #     pass

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
