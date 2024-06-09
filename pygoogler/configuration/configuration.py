"""Module to store project configurations."""

from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from .model import ConfigurationModel


class Configuration(BaseSettings, ConfigurationModel):
    """Project settings."""

    model_config = SettingsConfigDict(json_file="config.json")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customise the settings sources."""
        return (JsonConfigSettingsSource(settings_cls),)


configuration: Configuration = Configuration()
