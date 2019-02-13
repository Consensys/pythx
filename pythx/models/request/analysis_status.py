import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.util import dict_delete_none_fields


class AnalysisStatusRequest:
    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    def method(self):
        return "GET"

    @property
    def endpoint(self):
        return "v1/analyses/{}".format(self.uuid)

    @property
    def parameters(self):
        return {}

    @property
    def payload(self):
        return {}

    @classmethod
    def from_json(cls, json_str: str):
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, d):
        uuid = d.get("uuid")
        if uuid is None:
            raise RequestDecodeError("Missing uuid field in data {}".format(d))
        return cls(uuid=uuid)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"uuid": self.uuid}
