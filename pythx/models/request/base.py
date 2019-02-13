import abc


class BaseRequest(abc.ABC):

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
