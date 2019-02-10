from typing import Dict, List

from pythx import config
from pythx.core.request import models as reqmodels
from pythx.core.response import models as respmodels
from pythx.middleware.base import BaseMiddleware


class APIHandler:
    def __init__(self, middlewares: List[BaseMiddleware] = None):
        middlewares = middlewares if middlewares is not None else []
        self.middlewares = middlewares

    @staticmethod
    def send_request(request_data: Dict):
        # get headers
        # get url
        # requests.get/post
        pass

    def assemble_analysis_list_request(
        self, req: reqmodels.AnalysisListRequest
    ) -> Dict:
        # model to dict
        # execute middlewares process_request()
        request_dict = {"payload": req.to_dict(), "headers": {}, "url": config[""]}

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
        pass

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
        pass

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
        pass

    def parse_analysis_issues_response(
        self, resp: str
    ) -> respmodels.DetectedIssuesResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_login_request(self, req: reqmodels.AuthLoginRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        pass

    def parse_auth_login_response(self, resp: str) -> respmodels.AuthLoginResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_logout_request(self, req: reqmodels.AuthLogoutRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        pass

    def parse_auth_logout_response(self, resp: str) -> respmodels.AuthLogoutResponse:
        # model from JSON
        # execute middlewares process_response()
        pass

    def assemble_auth_refresh_request(self, req: reqmodels.AuthRefreshRequest) -> Dict:
        # model to dict
        # execute middlewares process_request()
        pass

    def parse_auth_refresh_response(self, resp: str) -> respmodels.AuthRefreshResponse:
        # model from JSON
        # execute middlewares process_response()
        pass
