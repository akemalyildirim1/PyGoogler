"""E2E tests for main module."""

from json import loads

import pytest

from pygoogler.exceptions import InvalidAPIKeyError, NotFoundError
from pygoogler.main import app, ItemsList, search_service
from pygoogler.models import SearchResponse
from typer.testing import CliRunner

runner = CliRunner()


class TestHelp:
    def test_ok(self):
        result = runner.invoke(app, ["--help"])
        assert all(
            text in result.output
            for text in ["init", "start", "configure", "reset", "search"]
        )
        assert result.exit_code == 0


class TestStartAndInit:
    @pytest.mark.parametrize(
        "command",
        [
            ["start"],
            ["init"],
        ],
    )
    def test_ok(self, command):
        result = runner.invoke(app, command)
        assert "Welcome to the Google search CLI setup." in result.output
        assert "Creating an initial configuration file." in result.output
        assert "Configuration file created successfully." in result.output
        assert result.exit_code == 0


class TestReset:
    def test_ok(self):
        result = runner.invoke(app, ["reset"], input="y\n")
        assert "Are you sure you want to reset the configuration file?" in result.output
        assert "Configuration file reset successfully." in result.output
        assert result.exit_code == 0

    def test_abort(self):
        result = runner.invoke(app, ["reset"], input="n\n")
        assert "Are you sure you want to reset the configuration file?" in result.output
        assert "Resetting the configuration file aborted." in result.output
        assert result.exit_code == 1


class TestUpdateConfig:
    def test_ok(self):
        try:
            result = runner.invoke(
                app,
                ["configure"],
                input="test-api-key\ntest-engine-id\n",
            )
            assert "Configuration file updated successfully." in result.output
            assert result.exit_code == 0

            with open("config.json", "r") as f:
                data = loads(f.read())
                assert data["custom_search_api_key"] == "test-api-key"
                assert data["programmable_search_engine_id"] == "test-engine-id"
        finally:
            runner.invoke(app, ["reset"], input="y\n")


@pytest.fixture
def mock_search_service(mocker):
    """Fixture for creating a mocked search service."""
    return mocker.patch.object(
        search_service,
        "main",
        autospec=True,
    )


@pytest.fixture
def mock_items_list(mocker):
    """Fixture for creating a mocked ItemsList."""
    return mocker.patch.object(
        ItemsList,
        "__call__",
        autospec=True,
    )


class TestSearch:
    def test_ok(self, mocker, mock_items_list, mock_search_service):
        mock_launch = mocker.patch("typer.launch")
        mock_launch.return_value = None

        response = [
            SearchResponse(
                title="Test title",
                link="https://test.com",
                snippet="Test snippet",
            )
        ]
        mock_search_service.return_value = response
        mock_items_list.return_value = response[0]
        result = runner.invoke(
            app,
            ["search", "test"],
        )
        assert result.exit_code == 0
        mock_launch.assert_called_once_with("https://test.com")

    def test_no_results(self, mock_search_service):
        mock_search_service.side_effect = NotFoundError()
        result = runner.invoke(
            app,
            ["search", "test"],
        )
        assert result.exit_code == 1
        assert "No search results found." in result.output

    def test_invalid_api_key(self, mock_search_service):
        mock_search_service.side_effect = InvalidAPIKeyError()
        result = runner.invoke(
            app,
            ["search", "test"],
        )
        assert result.exit_code == 1
        assert "Your credentials are invalid." in result.output

    def test_abort(self, mock_search_service, mock_items_list):
        mock_search_service.return_value = []
        mock_items_list.return_value = []
        result = runner.invoke(
            app,
            ["search", "test"],
        )
        assert result.exit_code == 1
        assert "Application closed." in result.output
