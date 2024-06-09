"""Unit tests for configuration service."""

from json import load
from pathlib import Path

import pytest

from pygoogler.configuration import ConfigurationModel
from pygoogler.service.configuration import ConfigurationService


@pytest.fixture
def configuration_service() -> ConfigurationService:
    """Create a configuration service instance."""
    return ConfigurationService()


class TestWriteToFile:
    def test_write_to_file(self, configuration_service: ConfigurationService):
        file_path = Path("tests/unit/service/configuration.json")
        try:
            configuration_service._write_to_file(
                configuration_file_path=file_path,
                configuration=ConfigurationModel(
                    custom_search_api_key="test-api-key",
                    programmable_search_engine_id="test-engine-id",
                ),
            )

            with open(file_path, "rb") as file:
                config_data = load(file)

            assert config_data["custom_search_api_key"] == "test-api-key"
            assert config_data["programmable_search_engine_id"] == "test-engine-id"
        finally:
            file_path.unlink()
