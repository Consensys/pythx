import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestValidationError
from pythx.models.request.analysis_status import AnalysisStatusRequest
from pythx.models.util import dict_delete_none_fields


class DetectedIssuesRequest(AnalysisStatusRequest):
    def __init__(self, uuid: str):
        super().__init__(uuid)
        self.uuid = uuid

    @property
    def endpoint(self):
        return "v1/analyses/{}/issues".format(self.uuid)

    @property
    def method(self):
        return "GET"

    @property
    def parameters(self):
        return {}
