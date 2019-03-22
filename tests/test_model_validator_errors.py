import pytest

from pythx.models import response as respmodels
from pythx.models import request as reqmodels
from pythx.models.exceptions import RequestValidationError, ResponseValidationError
from . import common as testdata


@pytest.mark.parametrize(
    "r_dict,model,should_raise,exc",
    [
        (testdata.ANALYSIS_LIST_REQUEST_DICT, reqmodels.AnalysisListRequest, False, RequestValidationError),
        (testdata.DETECTED_ISSUES_REQUEST_DICT, reqmodels.DetectedIssuesRequest, False, RequestValidationError),
        (testdata.ANALYSIS_STATUS_REQUEST_DICT, reqmodels.AnalysisStatusRequest, False, RequestValidationError),
        (testdata.ANALYSIS_SUBMISSION_REQUEST_DICT, reqmodels.AnalysisSubmissionRequest, True, RequestValidationError),
        (testdata.LOGIN_REQUEST_DICT, reqmodels.AuthLoginRequest, True, RequestValidationError),
        (testdata.LOGOUT_REQUEST_DICT, reqmodels.AuthLogoutRequest, True, RequestValidationError),
        (testdata.REFRESH_REQUEST_DICT, reqmodels.AuthRefreshRequest, True, RequestValidationError),
        (testdata.ANALYSIS_LIST_RESPONSE_DICT, respmodels.AnalysisListResponse, True, ResponseValidationError),
        (testdata.DETECTED_ISSUES_RESPONSE_DICT, respmodels.DetectedIssuesResponse, True, ResponseValidationError),
        (testdata.ANALYSIS_STATUS_RESPONSE_DICT, respmodels.AnalysisStatusResponse, True, ResponseValidationError),
        (testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT, respmodels.AnalysisSubmissionResponse, True, ResponseValidationError),
        (testdata.LOGIN_RESPONSE_DICT, respmodels.AuthLoginResponse, True, ResponseValidationError),
        (testdata.LOGOUT_RESPONSE_DICT, respmodels.AuthLogoutResponse, False, ResponseValidationError),
        (testdata.REFRESH_RESPONSE_DICT, respmodels.AuthRefreshResponse, True, ResponseValidationError),
    ],
)
def test_model_validators(r_dict, model, should_raise, exc):
    if should_raise:
        with pytest.raises(exc):
            model.validate({})
    else:
        model.validate(r_dict)
