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
        self.endpoint_conf = config["endpoints"][self.mode]

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

    def get_full_endpoint_url(self, keys: List[str]) -> str:
        d = self.endpoint_conf
        base = d["base"]
        for key in keys:
            d = d[key]
        return urllib.parse.urljoin(base, d)

    def assemble_analysis_list_request(
        self, req: reqmodels.AnalysisListRequest
    ) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["analysis", "list"])
        base_request = {
            "method": "get",
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)

    def parse_analysis_list_response(
        self, resp: str
    ) -> respmodels.AnalysisListResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_analysis_submission_request(
        self, req: reqmodels.AnalysisSubmissionRequest
    ) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["analysis", "submission"])
        base_request = {
            "method": "post",
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)

    def parse_analysis_submission_response(
        self, resp: str
    ) -> respmodels.AnalysisSubmissionResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_analysis_status_request(
        self, req: reqmodels.AnalysisStatusRequest
    ) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["analysis", "status"])
        base_request = {
            "method": "get",
            "payload": req.payload(),
            "headers": {},
            "url": url.format(req.uuid),
        }
        return self.execute_request_middlewares(base_request)

    def parse_analysis_status_response(
        self, resp: str
    ) -> respmodels.AnalysisStatusResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_analysis_issues_request(
        self, req: reqmodels.DetectedIssuesRequest
    ) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["analysis", "issues"])
        base_request = {
            "method": "get",
            "payload": req.payload(),
            "headers": {},
            "url": url.format(req.uuid),
        }
        return self.execute_request_middlewares(base_request)

    def parse_analysis_issues_response(
        self, resp: str
    ) -> respmodels.DetectedIssuesResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_login_request(self, req: reqmodels.AuthLoginRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["auth", "login"])
        base_request = {
            "method": "post",
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)

    def parse_auth_login_response(self, resp: str) -> respmodels.AuthLoginResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_logout_request(self, req: reqmodels.AuthLogoutRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["auth", "logout"])
        base_request = {
            "method": "post",
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)

    def parse_auth_logout_response(self, resp: str) -> respmodels.AuthLogoutResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_refresh_request(self, req: reqmodels.AuthRefreshRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        url = self.get_full_endpoint_url(["analysis", "status"])
        base_request = {
            "method": "post",
            "payload": req.payload(),
            "headers": {},
            "url": url,
        }
        return self.execute_request_middlewares(base_request)

    def parse_auth_refresh_response(self, resp: str) -> respmodels.AuthRefreshResponse:
        # model from JSON
        # execute middlewares process_response()
        pass
