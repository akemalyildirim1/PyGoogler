"""Service factory module."""

from functools import lru_cache

from pygoogler.search_api import SearchAPI

from .configuration import ConfigurationService
from .search import SearchService


class ServiceFactory:
    """Service factory class."""

    @staticmethod
    @lru_cache(maxsize=1)
    def create_configuration_service() -> ConfigurationService:
        """Create configuration service.

        Returns:
            ConfigurationModel: The configuration service.
        """
        return ConfigurationService()

    @staticmethod
    @lru_cache(maxsize=1)
    def create_search_service(search_api: SearchAPI) -> SearchService:
        """Create search service.

        Returns:
            SearchService: The search service.
        """
        return SearchService(search_api=search_api)
