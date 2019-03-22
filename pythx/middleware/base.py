import abc


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    def process_request(self, req):
        """

        :param req:
        """
        pass

    @abc.abstractmethod
    def process_response(self, resp):
        """

        :param resp:
        """
        pass
