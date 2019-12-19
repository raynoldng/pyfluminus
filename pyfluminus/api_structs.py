from pyfluminus.constants import ErrorTypes
from typing import TypeVar, Generic

Value = TypeVar("Value")
Error = TypeVar("Error")


class BaseResult(Generic[Value, Error]):
    """base container for response from API calls
    """

    def __init__(self, data: Value, error_type: Error, error_msg=None):
        self.data = data
        self.error_type = error_type
        self.error_msg = error_msg

    @property
    def ok(self) -> bool:
        # not sufficient to use data since can return an empty result
        return self.error_type is None


class Result(BaseResult[Value, None]):
    """contains the response from API calls"""

    def __init__(self, data: Value, error_type=None, error_msg=None):
        self.data = data
        self.error_type = error_type
        self.error_msg = error_msg


EmptyResultType = Result[None]


def EmptyResult() -> EmptyResultType:
    """helper function for returning an empty Result, ducks like a class constructor
    """
    return Result(None)


class ErrorResult(Result):
    """convenience wrapper for initializing Error results"""

    def __init__(self, error_type=ErrorTypes.Error, error_msg=None):
        super().__init__(data=None, error_type=error_type, error_msg=error_msg)
