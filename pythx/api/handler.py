import urllib.parse
from typing import Dict, List

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

    def execute_response_middlewares(self, resp):
        for mw in self.middlewares:
            resp = mw.process_response(resp)
        return resp

    def parse_response(self, resp: str, model):
        m = model.from_json(resp)
        return self.execute_response_middlewares(m)

    def assemble_request(self, req):
        url = urllib.parse.urljoin(config["endpoints"][self.mode], req.endpoint)
        base_request = {
            "method": req.method,
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)
