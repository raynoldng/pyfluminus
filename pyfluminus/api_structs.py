from pyfluminus.constants import ErrorTypes


class Result:
    """contains the response from API calls"""

    def __init__(self, data=None, error_type=None, error_msg=None):
        self.data = data
        self.error_type = error_type
        self.error_msg = error_msg

    @property
    def okay(self):
        # not sufficient to use data since can return an empty result
        return self.error_type is None


class ErrorResult(Result):
    """convenience wrapper for initializing Error results"""

    def __init__(self, error_type=ErrorTypes.Error, error_msg=None):
        super().__init__(data=None, error_type=error_type, error_msg=error_msg)
