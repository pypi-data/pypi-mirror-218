"""This Python module contains the User dataclass.

Classes:
    PexelsUser: A dataclass containing information about a specific user.
"""

# Imports
from dataclasses import dataclass


# User class
@dataclass
class PexelsUser:
    """A dataclass containing information about a specific user.

    Attributes:
        name: The name of the user.
        url: The URL of the user's profile.
        pexels_id: The Pexels ID of the user.
        username: The username of the user (with the @).
    """

    _name: str
    _url: str
    _pexels_id: int

    # Properties
    @property
    def name(self) -> str:
        """The name of the user."""
        return self._name

    @property
    def url(self) -> str:
        """The URL of the user's profile."""
        return self._url

    @property
    def pexels_id(self) -> int:
        """The Pexels ID of the user."""
        return self._pexels_id

    @property
    def username(self) -> str:
        """The username of the user (with the @)."""
        return "@" + self.url.split("@")[1]
