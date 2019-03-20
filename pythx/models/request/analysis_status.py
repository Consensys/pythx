from pythx.models.exceptions import RequestDecodeError
from pythx.models.request.base import BaseRequest


class AnalysisStatusRequest(BaseRequest):
    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    def method(self):
        return "GET"

    @property
    def endpoint(self):
        return "v1/analyses/{}".format(self.uuid)

    @property
    def headers(self):
        return {}

    @property
    def parameters(self):
        return {}

    @property
    def payload(self):
        return {}

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d):
        uuid = d.get("uuid")
        if uuid is None:
            raise RequestDecodeError("Missing uuid field in data {}".format(d))
        return cls(uuid=uuid)

    def to_dict(self):
        return {"uuid": self.uuid}
