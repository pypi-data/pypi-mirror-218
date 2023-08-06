"""This small Python module contains the endpoints that are accessed by a PexelsSession object in an HTTPS request.

Variables:
    ENDPOINTS: A dictionary of all endpoints used by the PexelsSession class.
"""

ENDPOINTS = {
    "FIND_PHOTO": "https://api.pexels.com/v1/photos",
    "FIND_VIDEO": "https://api.pexels.com/videos/videos",
    "CURATED_PHOTOS": "https://api.pexels.com/v1/curated",
    "POPULAR_VIDEOS": "https://api.pexels.com/videos/popular",
    "FEATURED_COLLECTIONS": "https://api.pexels.com/v1/collections/featured",
    "USER_COLLECTIONS": "https://api.pexels.com/v1/collections",
    "COLLECTION_MEDIA": "https://api.pexels.com/v1/collections",
    "SEARCH_PHOTOS": "https://api.pexels.com/v1/search",
    "SEARCH_VIDEOS": "https://api.pexels.com/videos/search"
}
