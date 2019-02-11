from typing import Dict, List
import urllib.parse

from pythx import config
from pythx.core.request import models as reqmodels
from pythx.core.response import models as respmodels
from pythx.middleware.base import BaseMiddleware


class APIHandler:
    def __init__(self, middlewares: List[BaseMiddleware] = None, staging: bool = False):
        middlewares = middlewares if middlewares is not None else []
        self.middlewares = middlewares
        self.mode = "staging" if staging else "production"

    @staticmethod
    def send_request(request_data: Dict):
        # get headers
        # get url
        # requests.get/post
        pass

    def execute_request_middlewares(self, req):
        for mw in self.middlewares:
            req = mw.process_request(req)
        return req

    @staticmethod
    def parse_response(resp: str, model):
        return model.from_json(resp)

    def assemble_request(self, req):
        url = urllib.parse.urljoin(config["endpoints"][self.mode], req.endpoint)
        base_request = {
            "method": req.method,
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)
