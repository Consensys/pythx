import logging
from pythx.middleware.base import BaseMiddleware


LOGGER = logging.getLogger("ClientToolNameMiddleware")


class ClientToolNameMiddleware(BaseMiddleware):
    """

    """
    def __init__(self, name="pythx"):
        LOGGER.debug("Initializing")
        self.name = name

    def process_request(self, req):
        """

        :param req:
        :return:
        """
        if req["method"] == "POST" and req["url"].endswith("/analyses"):
            LOGGER.debug("Adding name %s to request", self.name)
            req["payload"]["clientToolName"] = self.name
        return req

    def process_response(self, resp):
        """

        :param resp:
        :return:
        """
        LOGGER.debug("Forwarding the response without any action")
        return resp
