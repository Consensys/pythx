from pythx.models.request.base import BaseRequest


class VersionRequest(BaseRequest):
    @property
    def endpoint(self):
        return "v1/version"

    @property
    def method(self):
        return "GET"

    @property
    def payload(self):
        return {}

    @property
    def parameters(self):
        return {}

    @property
    def headers(self):
        return {}

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, d):
        return cls()

    def to_dict(self):
        return {}
