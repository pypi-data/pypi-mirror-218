"""This Python module contains the PexelsQueryResults dataclass.

Classes:
    PexelsQueryResults: The dataclass that contains the results of a query made by a PexelsSession object.
"""

# Imports
from dataclasses import dataclass
from .photo import PexelsPhoto
from .video import PexelsVideo
from .collection import PexelsCollection


# Class
@dataclass
class PexelsQueryResults:
    """The dataclass that contains the results of a query made by a PexelsSession object.

    Attributes:
        content: The list of photos/pictures/collections returned by the query.
        url: The URL of the query.
        total_results: The total amount of results received from the query.
        page: The page number of the query.
        per_page: The amount of content returned per page.
    """

    _content: list
    _url: str
    _total_results: int
    _page: int
    _per_page: int

    # Properties
    @property
    def content(self) -> list[PexelsPhoto | PexelsVideo | PexelsCollection]:
        """The list of photos/pictures/collections returned by the query."""
        return self._content

    @property
    def url(self) -> str:
        """The URL of the query."""
        return self._url

    @property
    def total_results(self) -> int:
        """The total amount of results received from the query."""
        return self._total_results

    @property
    def page(self) -> int:
        """The page number of the query."""
        return self._page

    @property
    def per_page(self) -> int:
        """The amount of content returned per page."""
        return self._per_page
