"""This Python module contains the PexelsVideoPicture dataclass.

Classes:
    PexelsVideoPicture: The dataclass that contains information about a preview picture of a Pexels video.
"""

# Imports
from dataclasses import dataclass


# Class
@dataclass
class PexelsVideoPicture:
    """The dataclass that contains information about a preview picture of a Pexels video.

    Attributes:
        pexels_id: The ID of the preview picture.
        picture_url: The URL of the preview picture.

    """

    _pexels_id: int
    _picture_url: str

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the preview picture."""
        return self._pexels_id

    @property
    def picture_url(self) -> str:
        """The URL of the preview picture."""
        return self._picture_url
