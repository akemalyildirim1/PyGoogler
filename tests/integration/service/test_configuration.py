"""Integration tests for configuration service."""

from pathlib import Path

import pytest

from pygoogler.configuration import ConfigurationModel

from tests.unit.service.test_configuration import configuration_service

_ = configuration_service


@pytest.fixture
def mock_write_to_file(mocker, configuration_service):
    return mocker.patch.object(configuration_service, "_write_to_file", autospec=True)


class TestResetConfiguration:
    def test_reset_configuration(self, mock_write_to_file, configuration_service):
        config_path = Path("config.json")
        configuration_service.reset_config(configuration_file_path=config_path)

        mock_write_to_file.assert_called_once_with(
            configuration_file_path=config_path,
            configuration=ConfigurationModel(
                custom_search_api_key="YOUR-API-KEY",
                programmable_search_engine_id="YOUR-ENGINE-ID",
            ),
        )


class TestUpdateConfiguration:
    def test_update(self, mock_write_to_file, configuration_service):
        config_path = Path("config.json")
        configuration = ConfigurationModel(
            custom_search_api_key="updated-api-key",
            programmable_search_engine_id="updated-engine-id",
        )
        configuration_service.update_config(
            configuration_file_path=config_path, configuration=configuration
        )

        mock_write_to_file.assert_called_once_with(
            configuration_file_path=config_path, configuration=configuration
        )
