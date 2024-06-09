"""Unit tests for google search API."""

import pytest

from pygoogler.exceptions import InvalidAPIKeyError, NotFoundError
from pygoogler.models import SearchResponse
from pygoogler.search_api.google import GoogleSearchAPI


@pytest.fixture
def google_search_api() -> GoogleSearchAPI:
    """Fixture for google search API."""
    return GoogleSearchAPI()


@pytest.fixture
def mock_response(mocker):
    def _mock_response(ok=True, json_data=None):
        mock_res = mocker.patch("pygoogler.search_api.google.requests_get")
        mock_res.return_value.ok = ok
        mock_res.return_value.json.return_value = json_data
        return mock_res

    return _mock_response


class TestSearch:
    def test_search(self, mock_response, google_search_api: GoogleSearchAPI):
        mock_response(
            ok=True,
            json_data={
                "items": [
                    {
                        "title": "Title 1",
                        "link": "www.link1.com",
                        "snippet": "Snippet 1",
                    },
                    {
                        "title": "Title 2",
                        "link": "www.link2.com",
                        "snippet": "Snippet 2",
                    },
                ]
            },
        )
        search_responses = google_search_api.search("News")

        assert isinstance(search_responses, list)
        assert all(
            [isinstance(response, SearchResponse) for response in search_responses]
        )
        assert len(search_responses) == 2
        assert search_responses[0] == SearchResponse(
            title="Title 1", link="www.link1.com", snippet="Snippet 1"
        )
        assert search_responses[1] == SearchResponse(
            title="Title 2", link="www.link2.com", snippet="Snippet 2"
        )

    def test_should_raise_invalid_api_key_error(
        self, mock_response, google_search_api: GoogleSearchAPI
    ):
        mock_response(ok=False, json_data={"error": {"message": "Invalid API key"}})

        with pytest.raises(InvalidAPIKeyError) as exception:
            google_search_api.search("News")

        assert str(exception.value) == "Invalid API key"

    def test_should_raise_not_found_error(
        self, mock_response, google_search_api: GoogleSearchAPI
    ):
        mock_response(ok=True, json_data={"items": []})

        with pytest.raises(NotFoundError) as exception:
            google_search_api.search("News")

        assert str(exception.value) == "No results found."
