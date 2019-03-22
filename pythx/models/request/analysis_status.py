from pythx.models.exceptions import RequestValidationError
from pythx.models.request.base import BaseRequest


class AnalysisStatusRequest(BaseRequest):
    """

    """
    def __init__(self, uuid: str):
        self.uuid = uuid

    @property
    def method(self):
        """

        :return:
        """
        return "GET"

    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/analyses/{}".format(self.uuid)

    @property
    def headers(self):
        """

        :return:
        """
        return {}

    @property
    def parameters(self):
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
    def from_dict(cls, d):
        """

        :param d:
        :return:
        """
        uuid = d.get("uuid")
        if uuid is None:
            raise RequestValidationError("Missing uuid field in data {}".format(d))
        return cls(uuid=uuid)

    def to_dict(self):
        """

        :return:
        """
        return {"uuid": self.uuid}
