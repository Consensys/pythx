from datetime import datetime
from typing import Dict, List

from pythx import config
from pythx.api.handler import APIHandler
from pythx.models import request as reqmodels
from pythx.models import response as respmodels


class Client:
    def __init__(self, eth_address: str, password: str, handler: APIHandler = None):
        self.eth_address = eth_address
        self.password = password
        self.handler = handler or APIHandler()

        self.access_token = None
        self.refresh_token = None
        self.last_auth_ts = None

        self.login()

    def _assemble_send_parse(self, req_obj, resp_model, authentication=True):
        auth_header = {}
        if authentication:
            self._assert_authenticated()
            auth_header = {"Authorization": "Bearer {}".format(self.access_token)}
        req_dict = self.handler.assemble_request(req_obj)
        resp = self.handler.send_request(req_dict, auth_header=auth_header)
        return self.handler.parse_response(resp, resp_model)

    def _assert_authenticated(self):
        now = datetime.now()
        access_expiration = self.last_auth_ts + config["timeouts"]["access"]
        refresh_expiration = self.last_auth_ts + config["timeouts"]["refresh"]

        if now < access_expiration:
            # auth token still valid - continue
            return
        elif access_expiration < now < refresh_expiration:
            # access token expired, but refresh token hasn't - use it to get new access token
            self.refresh()
        else:
            # refresh token has also expired - let's login again
            self.login()

    def login(self):
        req = reqmodels.AuthLoginRequest(
            eth_address=self.eth_address, password=self.password, user_id=""
        )
        resp_model = self._assemble_send_parse(req, respmodels.AuthLoginResponse)
        self.access_token = resp_model.access_token
        self.refresh_token = resp_model.refresh_token
        self.last_auth_ts = datetime.now()
        return resp_model

    def logout(self):
        req = reqmodels.AuthLogoutRequest()
        return self._assemble_send_parse(req, respmodels.AuthLogoutResponse)

    def refresh(self):
        req = reqmodels.AuthRefreshRequest(
            access_token=self.access_token, refresh_token=self.refresh_token
        )
        resp_model = self._assemble_send_parse(req, respmodels.AuthRefreshResponse)
        self.access_token = resp_model.access_token
        self.refresh_token = resp_model.refresh_token
        return resp_model

    def analysis_list(self, date_from: datetime, date_to: datetime):
        req = reqmodels.AnalysisListRequest(
            offset=0, date_from=date_from, date_to=date_to
        )
        return self._assemble_send_parse(req, respmodels.AnalysisListResponse)

    def analyze(
        self,
        contract_name: str = None,
        bytecode: str = None,
        source_map: str = None,
        deployed_bytecode: str = None,
        deployed_source_map: str = None,
        sources: Dict[str, Dict[str, str]] = None,
        source_list: List[str] = None,
        solc_version: str = None,
        analysis_mode: str = "quick",
    ):
        req = reqmodels.AnalysisSubmissionRequest(
            contract_name=contract_name,
            bytecode=bytecode,
            source_map=source_map,
            deployed_bytecode=deployed_bytecode,
            deployed_source_map=deployed_source_map,
            sources=sources,
            source_list=source_list,
            solc_version=solc_version,
            analysis_mode=analysis_mode,
        )
        return self._assemble_send_parse(req, respmodels.AnalysisSubmissionResponse)

    def status(self, uuid: str):
        req = reqmodels.AnalysisStatusRequest(uuid)
        return self._assemble_send_parse(req, respmodels.AnalysisStatusResponse)

    def analysis_ready(self, uuid: str):
        resp = self.status(uuid)
        return (
            resp.status == respmodels.AnalysisStatus.FINISHED
            or resp.status == respmodels.AnalysisStatus.ERROR
        )

    def report(self, uuid: str):
        req = reqmodels.DetectedIssuesRequest(uuid)
        return self._assemble_send_parse(req, respmodels.DetectedIssuesResponse)

    def openapi(self, mode="yaml"):
        req = reqmodels.OASRequest(mode=mode)
        return self._assemble_send_parse(req, respmodels.OASResponse)

    def version(self):
        req = reqmodels.VersionRequest()
        return self._assemble_send_parse(req, respmodels.VersionResponse)
