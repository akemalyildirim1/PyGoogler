"""Configuration service module."""

from json import dumps
from pathlib import Path

from pygoogler.configuration import ConfigurationModel

from .service import Service


class ConfigurationService(Service):
    """Configuration service class."""

    def reset_config(self, configuration_file_path: Path) -> None:
        """Reset configurations.

        Arguments:
            configuration_file_path: The configuration file path.

        Returns:
            None.
        """
        configuration: ConfigurationModel = ConfigurationModel(
            custom_search_api_key="YOUR-API-KEY",
            programmable_search_engine_id="YOUR-ENGINE-ID",
        )
        self._write_to_file(
            configuration_file_path=configuration_file_path,
            configuration=configuration,
        )

    def update_config(
        self, configuration_file_path: Path, configuration: ConfigurationModel
    ) -> None:
        """Configure json file.

        Arguments:
            configuration_file_path: The configuration file path.
            configuration: The configuration to update.

        Returns:
            None.
        """
        self._write_to_file(
            configuration_file_path=configuration_file_path,
            configuration=configuration,
        )

    def _write_to_file(
        self, configuration_file_path: Path, configuration: ConfigurationModel
    ) -> None:
        """Write the data to the configuration file.

        Arguments:
            configuration_file_path: The configuration file path.
            configuration: The configuration to write to the file.

        Returns:
            None.
        """
        with open(configuration_file_path, "wb") as file:
            file.write(
                dumps(configuration.model_dump(), ensure_ascii=False, indent=4).encode(
                    "utf-8"
                )
            )
