import json
from typing import Dict

from pythx.models.request.base import BaseRequest
from pythx.models.util import resolve_schema


class AuthLogoutRequest(BaseRequest):
    """

    """
    with open(resolve_schema(__file__, "auth-logout.json")) as sf:
        schema = json.load(sf)

    def __init__(self, global_: bool = False):
        self.global_ = global_

    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/auth/logout"

    @property
    def method(self):
        """

        :return:
        """
        return "POST"

    @property
    def parameters(self):
        """

        :return:
        """
        return {}

    @property
    def headers(self):
        """

        :return:
        """
        return {}

    @property
    def payload(self):
        """

        :return:
        """
        return {}

    @classmethod
    def from_dict(cls, d: Dict):
        """

        :param d:
        :return:
        """
        cls.validate(d)
        return cls(global_=d["global"])

    def to_dict(self):
        """

        :return:
        """
        d = {"global": self.global_}
        self.validate(d)
        return d
