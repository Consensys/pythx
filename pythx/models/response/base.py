import abc
import json
import logging

import jsonschema

from pythx.models.exceptions import ResponseValidationError


LOGGER = logging.getLogger(__name__)


class BaseResponse(abc.ABC):
    schema = None

    @classmethod
    def validate(cls, candidate):
        """

        :param candidate:
        :return:
        """
        if cls.schema is None:
            LOGGER.warning("Cannot validate {} without a schema".format(cls.__name__))
            return
        try:
            jsonschema.validate(candidate, cls.schema)
        except jsonschema.ValidationError as e:
            raise ResponseValidationError(e)

    @classmethod
    def from_json(cls, json_str: str):
        """

        :param json_str:
        :return:
        """
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @abc.abstractclassmethod
    def from_dict(cls, d: dict):
        """

        :param d:
        """
        pass

    def to_json(self):
        """

        :return:
        """
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        """

        """
        pass
