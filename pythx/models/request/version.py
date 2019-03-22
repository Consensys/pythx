from pythx.models.request.base import BaseRequest


class VersionRequest(BaseRequest):
    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/version"

    @property
    def method(self):
        """

        :return:
        """
        return "GET"

    @property
    def payload(self):
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
    def headers(self):
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
        return cls()

    def to_dict(self):
        """

        :return:
        """
        return {}
