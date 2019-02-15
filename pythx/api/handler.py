import urllib.parse
from typing import Dict, List

import requests

from pythx import config
from pythx.middleware.base import BaseMiddleware
from pythx.models import request as reqmodels
from pythx.models import response as respmodels
from pythx.models.exceptions import PythXAPIError


class APIHandler:
    def __init__(self, middlewares: List[BaseMiddleware] = None, staging: bool = False):
        middlewares = middlewares if middlewares is not None else []
        self.middlewares = middlewares
        self.mode = "staging" if staging else "production"

    @staticmethod
    def send_request(request_data: Dict, auth_header: Dict[str, str] = None):
        if auth_header is None:
            auth_header = {}
        method = request_data["method"].upper()
        headers = request_data["headers"]
        headers.update(auth_header)
        url = request_data["url"]
        payload = request_data["payload"]
        params = request_data["params"]
        response = requests.request(
            method=method, url=url, headers=headers, data=payload, params=params
        )
        if response.status_code != 200:
            raise PythXAPIError(
                "Got unexpected status code {}: {}".format(
                    response.status_code, response.content
                )
            )
        return response.content

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
            "payload": req.payload,
            "params": req.parameters,
            "headers": req.headers,
            "url": url,
        }
        return self.execute_request_middlewares(base_request)