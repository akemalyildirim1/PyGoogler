"""Google search API implementation."""

from typing import Final

from pydantic import BaseModel

from requests import get as requests_get, Response
from typing_extensions import override

from pygoogler.configuration import configuration

from pygoogler.exceptions import InvalidAPIKeyError, NotFoundError
from ..models import SearchResponse, SearchResponses
from .search_api import SearchAPI


class SearchParameters(BaseModel):
    """Dataclass for storing search parameters.

    Attributes:
        key: Google custom search API key.
        cx: Programmable search engine ID.
        q: Query string.
    """

    key: str
    cx: str
    q: str


class GoogleSearchAPI(SearchAPI):
    """Google search API implementation."""

    custom_search_api_key: str = configuration.custom_search_api_key
    programmable_search_engine_id: str = configuration.programmable_search_engine_id

    URL: Final[str] = "https://www.googleapis.com/customsearch/v1"

    @override
    def search(self, query: str) -> SearchResponses:
        """Search for the given query.

        Arguments:
            query: Query string to search in google.

        Returns:
            List of search responses.

        Raises:
            NotFoundError: If no search results are found.
            InvalidAPIKeyError: If the given credentials is invalid.
        """
        parameters: SearchParameters = SearchParameters(
            key=self.custom_search_api_key,
            cx=self.programmable_search_engine_id,
            q=query,
        )

        response: Response = requests_get(self.URL, params=parameters.model_dump())

        if not response.ok:
            raise InvalidAPIKeyError(response.json()["error"]["message"])

        try:
            items: list = response.json()["items"]
            if not items:
                raise KeyError
            return [SearchResponse(**row) for row in items]
        except KeyError as e:
            raise NotFoundError from e
