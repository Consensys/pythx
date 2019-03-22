import logging
from datetime import datetime
from typing import Dict, List

import jwt

from pythx.api.handler import APIHandler
from pythx.middleware.toolname import ClientToolNameMiddleware
from pythx.models import request as reqmodels
from pythx.models import response as respmodels

LOGGER = logging.getLogger(__name__)


class Client:
    """The main class for API interaction.

    The client makes sure that you are authenticated at all times. For authentication data it
    required either the account's Ethereum address *and* password, or a valid combination of
    access *and* refresh token. If any token expires, the client will automatically try to
    refresh the access token, or log the user in again. After that, the original request is
    executed.

    Furthermore, the client class supports various actions for high-level usage to easily submit
    new analysis jobs, check their status, get notified whether they are ready, and fetch analysis
    job report data.
    """

    def __init__(
        self,
        eth_address: str = None,
        password: str = None,
        access_token: str = None,
        refresh_token: str = None,
        handler: APIHandler = None,
        staging: bool = False,
    ):
        self.eth_address = eth_address
        self.password = password
        self.handler = handler or APIHandler(
            middlewares=[ClientToolNameMiddleware()],
            staging=staging
        )

        self.access_token = access_token
        self.refresh_token = refresh_token

    def _assemble_send_parse(
        self, req_obj, resp_model, assert_authentication=True, include_auth_header=True
    ):
        """Assemble the request, send it, parse and return the response."""
        if assert_authentication:
            self.assert_authentication()
        auth_header = (
            {"Authorization": "Bearer {}".format(self.access_token)}
            if include_auth_header
            else {}
        )
        req_dict = self.handler.assemble_request(req_obj)
        LOGGER.debug("Sending request")
        resp = self.handler.send_request(req_dict, auth_header=auth_header)
        LOGGER.debug("Parsing response")
        return self.handler.parse_response(resp, resp_model)

    @staticmethod
    def _get_jwt_expiration_ts(token):
        """Decode the APIs JWT to get their expiration time."""
        return datetime.utcfromtimestamp((jwt.decode(token, verify=False)["exp"]))

    def assert_authentication(self):
        """Make sure the user is authenticated.

        If necessary, this method will refresh the access token, or perform another
        login to get a fresh combination of tokens if both are expired.

        :return: None
        """
        if self.access_token is None or self.refresh_token is None:
            # We haven't authenticated yet
            self.login()
            return
        now = datetime.utcnow()
        access_expiration = self._get_jwt_expiration_ts(self.access_token)
        refresh_expiration = self._get_jwt_expiration_ts(self.refresh_token)
        if now < access_expiration:
            # auth token still valid - continue
            LOGGER.debug(
                "Auth check passed, token still valid: {} < {}".format(
                    now, access_expiration
                )
            )
        elif access_expiration < now < refresh_expiration:
            # access token expired, but refresh token hasn't - use it to get new access token
            LOGGER.debug(
                "Auth refresh needed: {} < {} < {}".format(
                    access_expiration, now, refresh_expiration
                )
            )
            self.refresh(assert_authentication=False)
        else:
            # refresh token has also expired - let's login again
            LOGGER.debug("Access and refresh token have expired - logging in again")
            self.login()

    def login(self) -> respmodels.AuthLoginResponse:
        """Perform a login request on the API and return the response.

        :return: AuthLoginResponse
        """
        req = reqmodels.AuthLoginRequest(
            eth_address=self.eth_address, password=self.password
        )
        resp_model = self._assemble_send_parse(
            req,
            respmodels.AuthLoginResponse,
            assert_authentication=False,
            include_auth_header=False,
        )
        self.access_token = resp_model.access_token
        self.refresh_token = resp_model.refresh_token
        return resp_model

    def logout(self) -> respmodels.AuthLogoutResponse:
        """Perform a logout request on the API and return the response.

        :return: AuthLogoutResponse
        """
        req = reqmodels.AuthLogoutRequest()
        resp_model = self._assemble_send_parse(req, respmodels.AuthLogoutResponse)
        self.access_token = None
        self.refresh_token = None
        return resp_model

    def refresh(self, assert_authentication=True) -> respmodels.AuthRefreshResponse:
        """Perform a JWT refresh on the API and return the response.

        :param assert_authentication:
        :return: AuthRefreshResponse
        """
        req = reqmodels.AuthRefreshRequest(
            access_token=self.access_token, refresh_token=self.refresh_token
        )
        resp_model = self._assemble_send_parse(
            req,
            respmodels.AuthRefreshResponse,
            assert_authentication=False,
            include_auth_header=False,
        )
        self.access_token = resp_model.access_token
        self.refresh_token = resp_model.refresh_token
        return resp_model

    def analysis_list(
        self, date_from: datetime = None, date_to: datetime = None, offset: int = None
    ) -> respmodels.AnalysisListResponse:
        """Get a list of the user's analyses jobs.

        :param date_from: Start of the date range (optional)
        :param date_to: End of the date range (optional)
        :param offset: The number of results to skip (used for pagination)
        :return: AnalysisListResponse
        """
        req = reqmodels.AnalysisListRequest(
            offset=offset, date_from=date_from, date_to=date_to
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
    ) -> respmodels.AnalysisSubmissionResponse:
        """Submit a new analysis job.

        At least the smart contracts bytecode, or it's source code must be given. The more
        information the MythX API gets, the more precise and verbose the results will be.

        :param contract_name:
        :param bytecode:
        :param source_map:
        :param deployed_bytecode:
        :param deployed_source_map:
        :param sources:
        :param source_list:
        :param solc_version:
        :param analysis_mode:
        :return: AnalysisSubmissionResponse
        """
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
        # req.validate()
        return self._assemble_send_parse(req, respmodels.AnalysisSubmissionResponse)

    def status(self, uuid: str) -> respmodels.AnalysisStatusResponse:
        """Get the status of an analysis job based on its UUID.

        :param uuid: The job's UUID
        :return: AnalysisStatusResponse
        """
        req = reqmodels.AnalysisStatusRequest(uuid)
        return self._assemble_send_parse(req, respmodels.AnalysisStatusResponse)

    def analysis_ready(self, uuid: str) -> bool:
        """Return a boolean whether the analysis job with the given UUID has finished processing.

        :param uuid:
        :return: bool
        """
        resp = self.status(uuid)
        return (
            resp.analysis.status == respmodels.AnalysisStatus.FINISHED
            or resp.analysis.status == respmodels.AnalysisStatus.ERROR
        )

    def report(self, uuid: str) -> respmodels.DetectedIssuesResponse:
        """Get the report holding found issues for an analysis job based on its UUID.

        :param uuid:
        :return: DetectedIssuesResponse
        """
        req = reqmodels.DetectedIssuesRequest(uuid)
        return self._assemble_send_parse(req, respmodels.DetectedIssuesResponse)

    def openapi(self, mode="yaml") -> respmodels.OASResponse:
        """Return the OpenAPI specification either in HTML or YAML.

        :param mode: "yaml" or "html"
        :return: OASResponse
        """
        req = reqmodels.OASRequest(mode=mode)
        return self._assemble_send_parse(
            req,
            respmodels.OASResponse,
            assert_authentication=False,
            include_auth_header=False,
        )

    def version(self) -> respmodels.VersionResponse:
        """Call the APIs version endpoint to get its backend version numbers.

        :return: VersionResponse
        """
        req = reqmodels.VersionRequest()
        return self._assemble_send_parse(
            req,
            respmodels.VersionResponse,
            assert_authentication=False,
            include_auth_header=False,
        )

    def __enter__(self):
        self.assert_authentication()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()
