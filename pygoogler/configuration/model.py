"""Configuration model for the project."""

from pydantic import BaseModel, Field


class ConfigurationModel(BaseModel):
    """Configuration model for the project."""

    custom_search_api_key: str = Field(default="YOUR-API-KEY")
    programmable_search_engine_id: str = Field(default="YOUR-ENGINE-ID")
