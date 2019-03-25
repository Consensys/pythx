"""This module contains the base request domain model."""

import abc
import json
import logging

import jsonschema

from pythx.models.exceptions import RequestValidationError


LOGGER = logging.getLogger(__name__)


class BaseRequest(abc.ABC):
    """An abstract object describing requests to the MythX API."""

    schema = None

    @classmethod
    def validate(cls, candidate):
        """Validate the object's data format.

        This is done using a schema contained at the class level. If no schema is given, it is
        assumed that the request does not contain any meaningful data (e.g. a simple GET request
        without any parameters) and no validation is done.

        If the schema validation fails, a :code:`RequestValidationError` is raised.

        If this method is called on a concrete object that does not contain a schema,
        :code:`validate` will return right away and log a warning as this behaviour might not have
        been intended by a developer.

        :param candidate: The candidate dict to check the schema against
        :return: None
        """
        if cls.schema is None:
            LOGGER.warning("Cannot validate {} without a schema".format(cls.__name__))
            return
        try:
            jsonschema.validate(candidate, cls.schema)
        except jsonschema.ValidationError as e:
            raise RequestValidationError(e)

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize a given JSON string to the given domain model.

        Internally, this method uses the :code:`from_dict` method.

        :param json_str: The JSON string to deserialize
        :return: The concrete deserialized domain model instance
        """
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @abc.abstractclassmethod
    def from_dict(cls, d: dict):
        """An abstract method to construct the given domain model from a Python dict instance.

        :param d: The dict instance to deserialize
        """
        pass

    def to_json(self):
        """Serialize the current domain model instance to a JSON string.

        Internally, this method uses the :code:`to_dict` method.

        :return: The serialized domain model JSON string
        """
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        """An abstract method to serialize the current domain model instance to a Python dict.

        :return: A Python dict instance holding the serialized domain model data
        """
        pass

    @abc.abstractproperty
    def payload(self):
        """An abstract property returning the request's payload data.

        :return: A Python dict to be serialized into JSON format and submitted to the endpoint.
        """
        pass

    @abc.abstractproperty
    def headers(self):
        """An abstract property returning additional request headers.

        :return: A dict (str -> str) instance mapping header name to header content
        """
        pass

    @abc.abstractproperty
    def parameters(self):
        """An abstract property returning additional URL parameters

        :return: A dict (str -> str) instance mapping parameter name to parameter content
        """
        pass

    @abc.abstractproperty
    def method(self):
        """An abstract property returning the HTTP method to perform.

        :return: The uppercase HTTP method, e.g. "POST"
        """
        pass
