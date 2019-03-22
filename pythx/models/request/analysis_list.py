from datetime import datetime
from typing import Any, Dict

import dateutil.parser

from pythx.models.exceptions import RequestValidationError
from pythx.models.request.base import BaseRequest

ANALYSIS_LIST_KEYS = ("offset", "dateFrom", "dateTo")


class AnalysisListRequest(BaseRequest):
    """

    """
    def __init__(self, offset: int, date_from: datetime, date_to: datetime):
        self.offset = offset
        self.date_from = date_from
        self.date_to = date_to

    @property
    def endpoint(self):
        """

        :return:
        """
        return "v1/analyses"

    @property
    def method(self):
        """

        :return:
        """
        return "GET"

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
        return self.to_dict()

    @property
    def payload(self):
        """

        :return:
        """
        return {}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        """

        :param d:
        :return:
        """
        if not all(k in d for k in ANALYSIS_LIST_KEYS):
            raise RequestValidationError(
                "Not all required keys {} found in data {}".format(
                    ANALYSIS_LIST_KEYS, d
                )
            )
        req = cls(
            offset=d["offset"],
            date_from=dateutil.parser.parse(d["dateFrom"]),
            date_to=dateutil.parser.parse(d["dateTo"]),
        )

        return req

    def to_dict(self):
        """

        :return:
        """
        return {
            "offset": self.offset,
            "dateFrom": self.date_from.isoformat() if self.date_from else None,
            "dateTo": self.date_to.isoformat() if self.date_to else None,
        }
