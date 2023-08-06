"""This Python module contains the PexelsVideoPicture dataclass.

Classes:
    PexelsVideoFile: The class that contains data about a video file, of which there are many of, for one video
    uploaded to Pexels.
"""

# Imports
import requests


# Photo class
class PexelsVideoFile:
    """The class that contains data about a video file, of which there are many of, for one video uploaded to Pexels.

    Attributes:
        pexels_id: The Pexels ID of the video file.
        quality: The quality of the video file. Either "hd" or "sd".
        file_type: The video format of the video file.
        file_extension: The file extension of the video.
        size: A list containing the width and height of the video in pixels.
        fps: The number of FPS in the video file.
        url: A URL to where the video is being stored.

    Methods:
        download(self, path)
        Downloads the contents of the video to a given path.
    """

    def __init__(self, json_content: dict):
        """Constructor of the class.

        Args:
            json_content: A dictionary containing data about the video file for a given video after a successful API request.
        """

        # Initialization of attributes
        self._pexels_id = json_content["id"]
        self._quality = json_content["quality"]
        self._file_type = json_content["file_type"]
        self._size = [json_content["width"], json_content["height"]]
        self._fps = json_content["fps"]
        self._url = json_content["link"]

    # Methods
    def download(self, path):  # Path includes file name
        """Downloads the contents of the video to a given path."""
        video_content = requests.get(self.url)
        with open(f"{path}.{self.file_extension}", "wb") as file:
            file.write(video_content.content)

    # Properties
    @property
    def pexels_id(self) -> int:
        """The Pexels ID of the video file."""
        return self._pexels_id

    @property
    def quality(self) -> str:
        """The quality of the video file. Either "hd" or "sd"."""
        return self._quality

    @property
    def file_type(self) -> str:
        """The video format of the video file."""
        return self._file_type

    @property
    def file_extension(self) -> str:
        """The file extension of the video."""
        return self.file_type.split("/")[-1]

    @property
    def size(self) -> list[int]:
        """A list containing the width and height of the video in pixels."""
        return self._size

    @property
    def fps(self) -> float:
        """The number of FPS in the video file."""
        return self._fps

    @property
    def url(self) -> str:
        """A URL to where the video is being stored."""
        return self._url
