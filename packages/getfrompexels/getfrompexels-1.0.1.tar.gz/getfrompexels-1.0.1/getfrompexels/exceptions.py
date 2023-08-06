"""This Python module contains custom exceptions that are called in the case of an error.

Classes:
    PexelsAuthorizationError: Error that is raised when an API key is not given or is invalid but a request is called.
    PexelsSearchError: Error that is raised when a "search" function encounters an error.
    PexelsLookupError: Error that is raised when a "find" function encounters an error."
    PexelsAPIRequestError: More in-detail error that is raised when an HTTP response has an invalid status code after a request goes
    through the verify_response function.

"""


# Exceptions
class PexelsAuthorizationError(Exception):
    """Error that is raised when an API key is not given or is invalid but a request is called."""
    pass


class PexelsSearchError(Exception):
    """Error that is raised when a "search" function encounters an error."""
    pass


class PexelsLookupError(Exception):
    """Error that is raised when a "find" function encounters an error."""
    pass


class PexelsAPIRequestError(Exception):
    """More in-detail error that is raised when an HTTP response has an invalid status code after a request goes
    through the verify_response function."""
    pass
