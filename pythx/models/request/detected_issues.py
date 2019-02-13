import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request.analysis_status import AnalysisStatusRequest
from pythx.models.util import dict_delete_none_fields


class DetectedIssuesRequest(AnalysisStatusRequest):
    def __init__(self, uuid: str):
        super().__init__(uuid)

    @property
    def endpoint(self):
        return "v1/version"

    @property
    def method(self):
        return "GET"
