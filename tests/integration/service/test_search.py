"""Integration tests for search service."""

import pytest

from pygoogler.search_api import SearchAPI
from pygoogler.service.search import SearchService


@pytest.fixture
def mock_search_api(mocker):
    class MockSearchAPI(SearchAPI):
        def search(self, query: str):
            pass

    return mocker.Mock(spec=SearchAPI)


class TestSearch:
    def test_search(self, mock_search_api):
        search_service = SearchService(mock_search_api)
        search_service.main(query="Python")
        mock_search_api.search.assert_called_once_with(query="Python")
