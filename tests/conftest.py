"""Test configuration module."""

import json

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_config():
    """Setup configuration."""
    config_data = {
        "custom_search_api_key": "YOUR-API-KEY",
        "programmable_search_engine_id": "YOUR-ENGINE-ID",
    }
    with open("config.json", "wb") as file:
        file.write(json.dumps(config_data, indent=4).encode("utf-8"))
    yield
