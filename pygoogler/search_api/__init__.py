"""Module for storing the search engine API."""

from .google import GoogleSearchAPI
from .search_api import SearchAPI


__all__ = ["GoogleSearchAPI", "SearchAPI"]
