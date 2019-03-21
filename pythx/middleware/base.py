import abc


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    def process_request(self, req):
        pass

    @abc.abstractmethod
    def process_response(self, resp):
        pass
