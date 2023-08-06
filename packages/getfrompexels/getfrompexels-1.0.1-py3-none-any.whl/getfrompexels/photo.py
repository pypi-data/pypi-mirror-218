"""This Python module contains the PexelsPhoto class that holds information about a photo stored on Pexels.

Classes:
    PexelsPhoto: Class that contains information about a photo hosted on Pexels.
"""

# Imports
from .user import PexelsUser
import requests


# Photo class
class PexelsPhoto:
    """Class that contains information about a photo hosted on Pexels.

    Attributes:
        pexels_id: The ID of the photo.
        size: A list containing the width and height of the photo in pixels.
        pexels_url: The URL to the photo on Pexels.
        average_color: The hex code of the average color of the photo.
        photographer: PexelsUser object that contains information about the photographer.
        links: A dictionary containing direct links to the image in varying sizes.
        is_liked: A boolean variable that states whether the photo is liked by the user whose API is being used for the Session object. If the photo was returned from find_collection_contents() it is None as it doesn't appear to be returned properly when that method is called.
        alt_text: Alt text for the image.

    Methods:
        download(self, path, size="original")
        Downloads a JPG file of the image to a given path, allowing the user to pick a specific photo size if they wish.
    """

    def __init__(self, json_content: dict, hide_liked: bool = False):
        """Constructor of the class.

        Args:
            json_content: A dictionary containing data about the photo from a successful API request.
        """

        # Initialization of read-only attributes
        self._pexels_id = json_content["id"]
        self._size = [json_content["width"], json_content["height"]]
        self._pexels_url = json_content["url"]
        self._average_color = json_content["avg_color"]
        self._photographer = PexelsUser(
            json_content["photographer"],
            json_content["photographer_url"],
            json_content["photographer_id"]
        )
        self._links = {
            "original": json_content["src"]["original"],
            "large": json_content["src"]["large"],
            "large_2x": json_content["src"]["large2x"],
            "medium": json_content["src"]["medium"],
            "small": json_content["src"]["small"],
            "portrait": json_content["src"]["portrait"],
            "landscape": json_content["src"]["landscape"],
            "tiny": json_content["src"]["tiny"]
        }
        self._liked_by_user = json_content["liked"] if not hide_liked else None
        self._alt_text = json_content["alt"]

    # Methods
    def download(self, path: str, size: str = "original"):   # Path includes file name.
        """Downloads a JPG file of the image to a given path, allowing the user to pick a specific photo size if they
        wish.

        Args:
            path: The path and the filename of the file that the photo will be saved as. The .JPG extension will be added by default.
            size: The size of the photo that will be saved from the "links" property. Default is "original".
        """

        image_content = requests.get(self.links[size])
        with open(f"{path}.jpg", "wb") as file:
            file.write(image_content.content)

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the photo."""
        return self._pexels_id

    @property
    def size(self) -> list[int]:
        """A list containing the width and height of the photo in pixels."""
        return self._size

    @property
    def pexels_url(self) -> str:
        """The URL to the photo on Pexels."""
        return self._pexels_url

    @property
    def average_color(self) -> str:
        """The hex code of the average color of the photo."""
        return self._average_color

    @property
    def photographer(self) -> PexelsUser:
        """PexelsUser object that contains information about the photographer."""
        return self._photographer

    @property
    def links(self) -> dict:
        """A dictionary containing direct links to the image in varying sizes."""
        return self._links

    @property
    def liked_by_user(self) -> bool | None:
        """A boolean variable that states whether the photo is liked by the user whose API is being used for the Session object. If the photo was returned from find_collection_contents() it is None as it doesn't appear to be returned properly when that method is called."""
        return self._liked_by_user

    @property
    def alt_text(self) -> str:
        """Alt text for the image."""
        return self._alt_text
