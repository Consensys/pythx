from mythx_models import request as reqmodels
from mythx_models import response as respmodels
from typing import Union


RESPONSE_MODELS = Union[
    respmodels.AnalysisInputResponse,
    respmodels.AnalysisListResponse,
    respmodels.AnalysisStatusResponse,
    respmodels.AnalysisSubmissionResponse,
    respmodels.AuthLoginResponse,
    respmodels.AuthLogoutResponse,
    respmodels.AuthRefreshResponse,
    respmodels.DetectedIssuesResponse,
    respmodels.GroupCreationResponse,
    respmodels.GroupListResponse,
    respmodels.GroupOperationResponse,
    respmodels.GroupStatusResponse,
    respmodels.ProjectCreationResponse,
    respmodels.ProjectDeletionResponse,
    respmodels.ProjectListResponse,
    respmodels.ProjectStatusResponse,
    respmodels.ProjectUpdateResponse,
    respmodels.VersionResponse
]
REQUEST_MODELS = [
    reqmodels.AnalysisInputRequest,
    reqmodels.AnalysisListRequest,
    reqmodels.AnalysisStatusRequest,
    reqmodels.AnalysisSubmissionRequest,
    reqmodels.AuthLoginRequest,
    reqmodels.AuthLogoutRequest,
    reqmodels.AuthRefreshRequest,
    reqmodels.DetectedIssuesRequest,
    reqmodels.GroupCreationRequest,
    reqmodels.GroupListRequest,
    reqmodels.GroupOperationRequest,
    reqmodels.GroupStatusRequest,
    reqmodels.ProjectCreationRequest,
    reqmodels.ProjectDeleteRequest,
    reqmodels.ProjectListRequest,
    reqmodels.ProjectStatusRequest,
    reqmodels.ProjectUpdateRequest,
    reqmodels.VersionRequest
]
