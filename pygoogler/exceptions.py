"""Shared exceptions."""


class NotFoundError(ValueError):
    """Raised when a search query returns no results."""

    def __init__(self, message: str = "No results found."):
        """Initialize the class."""
        super().__init__(message)


class InvalidAPIKeyError(ValueError):
    """Raised when an invalid API key is provided."""

    def __init__(self, message: str = "Invalid API key."):
        """Initialize the class."""
        super().__init__(message)


class ApplicationClosedError(ValueError):
    """Raised when the application is closed."""

    def __init__(self, message: str = "Application closed."):
        """Initialize the class."""
