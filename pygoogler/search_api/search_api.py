"""Search API abstract class module."""

from abc import ABC, abstractmethod

from ..models import SearchResponses


class SearchAPI(ABC):
    """Search API abstract class."""

    @abstractmethod
    def search(self, query: str) -> SearchResponses:
        """Search for the given query.

        Arguments:
            query: The query to search for.

        Returns:
            The search results.
        """
