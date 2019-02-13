import abc


class BaseResponse(abc.ABC):

    @abc.abstractclassmethod
    def from_json(cls):
        pass

    @abc.abstractclassmethod
    def from_dict(cls):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def validate(self):
        pass
