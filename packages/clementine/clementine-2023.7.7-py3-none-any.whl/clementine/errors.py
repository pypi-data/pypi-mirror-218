"""Errors."""

from typing import Optional

__all__ = ["NotInstalledError"]


class NotInstalledError(ImportError):
    """Raised when a package is not installed."""

    def __init__(self, name: str, msg: Optional[str] = None):
        self.name = name
        self.msg = msg or f"The package '{name}' is not installed."
