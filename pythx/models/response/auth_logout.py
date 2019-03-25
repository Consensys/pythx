from typing import Dict

from pythx.models.exceptions import ResponseValidationError
from pythx.models.response.base import BaseResponse


class AuthLogoutResponse(BaseResponse):
    """The API response domain model for a successful logout action."""

    @classmethod
    def from_dict(cls, d: Dict):
        """Create the response domain model from a dict.

        This also validates the dict's schema and raises a :code:`ResponseValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        if not d == {}:
            raise ResponseValidationError(
                "The logout response should be empty but got data: {}".format(d)
            )
        return cls()

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
        d = {}
        return d
