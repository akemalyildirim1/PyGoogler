"""Search response module."""

from typing import TypeAlias

from pydantic import BaseModel


class SearchResponse(BaseModel):
    """Search response model.

    Attributes:
        title: The title of the search result.
        link: The link of the search result.
        snippet: The snippet of the search result.
    """

    title: str
    link: str
    snippet: str


SearchResponses: TypeAlias = list[SearchResponse]
