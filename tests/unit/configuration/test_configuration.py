"""Unit tests for configuration."""

from pygoogler.configuration import configuration


class TestGetConfiguration:
    def test_get_configuration(self):
        """Test get_configuration function."""
        assert configuration.custom_search_api_key == "YOUR-API-KEY"
        assert configuration.programmable_search_engine_id == "YOUR-ENGINE-ID"
