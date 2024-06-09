"""Search service module."""

from pygoogler.models import SearchResponses
from pygoogler.search_api import SearchAPI

from .service import Service


class SearchService(Service):
    """Search service."""

    def __init__(self, search_api: SearchAPI):
        """Initialize the class."""
        super().__init__()
        self.api: SearchAPI = search_api

    def main(self, query: str) -> SearchResponses:
        """Search given query.

        Arguments:
            query: Query ot search.

        Returns:
            Search responses.

        Raises:
            NotFoundError: If no search results are found.
            InvalidAPIKeyError: If the given credentials is invalid.
        """
        return self.api.search(query=query)
