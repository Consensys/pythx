import pytest

from pythx.models import response as respmodels
from pythx.models import request as reqmodels
from . import common as testdata


def generate_request_dict(req):
    return {
        "method": req.method,
        "payload": req.payload,
        "params": req.parameters,
        "headers": req.headers,
        "url": "https://test.com/" + req.endpoint,
    }


@pytest.mark.parametrize(
    "r_dict,model,should_raise",
    [
        (testdata.ANALYSIS_LIST_REQUEST_DICT, reqmodels.AnalysisListRequest, True),
        (testdata.DETECTED_ISSUES_REQUEST_DICT, reqmodels.DetectedIssuesRequest, True),
        (testdata.ANALYSIS_STATUS_REQUEST_DICT, reqmodels.AnalysisStatusRequest, True),
        (testdata.ANALYSIS_SUBMISSION_REQUEST_DICT, reqmodels.AnalysisSubmissionRequest, False),
        (testdata.LOGIN_REQUEST_DICT, reqmodels.AuthLoginRequest, False),
        (testdata.LOGOUT_REQUEST_DICT, reqmodels.AuthLogoutRequest, False),
        (testdata.REFRESH_REQUEST_DICT, reqmodels.AuthRefreshRequest, False),
        (testdata.ANALYSIS_LIST_RESPONSE_DICT, respmodels.AnalysisListResponse, False),
        (testdata.DETECTED_ISSUES_RESPONSE_DICT, respmodels.DetectedIssuesResponse, False),
        (testdata.ANALYSIS_STATUS_RESPONSE_DICT, respmodels.AnalysisStatusResponse, False),
        (testdata.ANALYSIS_SUBMISSION_RESPONSE_DICT, respmodels.AnalysisSubmissionResponse, False),
        (testdata.LOGIN_RESPONSE_DICT, respmodels.AuthLoginResponse, False),
        (testdata.LOGOUT_RESPONSE_DICT, respmodels.AuthLogoutResponse, True),
        (testdata.REFRESH_RESPONSE_DICT, respmodels.AuthRefreshResponse, False),
    ],
)
def test_model_validators(r_dict, model, should_raise):
    if should_raise:
        with pytest.raises(TypeError):
            model.validate(r_dict)
    else:
        model.validate(r_dict)
