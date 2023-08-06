"""This Python module contains the PexelsVideo class that holds information about a video stored on Pexels.

Classes:
    PexelsVideo: The class that contains information about a video on Pexels.
"""

# Imports
from .user import PexelsUser
from .video_file import PexelsVideoFile
from .video_picture import PexelsVideoPicture


# Video class
class PexelsVideo:
    """The class that contains information about a video on Pexels.

    Attributes:
        pexels_id: The ID of the video.
        size: A list containing the width and height of the video in pixels.
        pexels_url: The URL to the video on Pexels.
        screenshot_url: The URL to a screenshot of the video.
        duration: Duration of the video in seconds.
        owner: PexelsUser object that contains information about the video owner.
        video_files: A list of video files as PexelsVideoFile objects of the video.
        video_pictures: A list of preview pictures as PexelsVideoPicture objects of the video.
    """

    def __init__(self, json_content):
        """Constructor of the class.

        Args:
            json_content: A dictionary containing data about the video from a successful API request.
        """

        # Initialization of all read-only attributes
        self._pexels_id = json_content["id"]
        self._size = [json_content["width"], json_content["height"]]
        self._pexels_url = json_content["url"]
        self._screenshot_url = json_content["image"]
        self._duration = json_content["duration"]
        self._owner = PexelsUser(
            json_content["user"]["id"],
            json_content["user"]["name"],
            json_content["user"]["url"]
        )

        # Initialization continued; creation of lists with child classes
        video_files = json_content["video_files"]
        video_pictures = json_content["video_pictures"]
        self._video_files = [PexelsVideoFile(x) for x in video_files]
        self._video_pictures = [PexelsVideoPicture(x["id"], x["picture"]) for x in video_pictures]

    # Properties
    @property
    def pexels_id(self) -> int:
        """The ID of the video."""
        return self._pexels_id

    @property
    def size(self) -> list[int]:
        """A list containing the width and height of the video in pixels."""
        return self._size

    @property
    def pexels_url(self) -> str:
        """The URL to the video on Pexels."""
        return self._pexels_url

    @property
    def screenshot_url(self) -> str:
        """The URL to the video on Pexels."""
        return self._screenshot_url

    @property
    def duration(self) -> int:
        """Duration of the video in seconds."""
        return self._duration

    @property
    def owner(self) -> PexelsUser:
        """PexelsUser object that contains information about the video owner."""
        return self._owner

    @property
    def video_files(self) -> list[PexelsVideoFile]:
        """A list of video files as PexelsVideoFile objects of the video."""
        return self._video_files

    @property
    def video_pictures(self) -> list[PexelsVideoPicture]:
        """A list of preview pictures as PexelsVideoPicture objects of the video."""
        return self._video_pictures
