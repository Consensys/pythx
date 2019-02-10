import abc


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    def process_request(self):
        pass

    @abc.abstractmethod
    def process_response(self):
        pass
