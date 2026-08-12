# !/usr/bin/env python3

"""Application version and metadata management."""

# Single source of version info
__author__ = "@mikespon"
__last_updated__ = "12-Aug-2026"
__version__ = "0.3.2"
__license__ = "MIT"
__description__ = "KML creation from iOS location data utility"


def get_version_info() -> dict:
    """Return complete version information as a dictionary."""
    return {
        "version": __version__,
        "author": __author__,
        "last_updated": __last_updated__,
        "license": __license__,
        "description": __description__
    }


def get_version_string(short: bool = False) -> str:
    """Return formatted version string.

    Args:
        short: If True, return only version number (e.g., "0.4.1785974400").
        If False, return full banner.

    Returns:
        Formatted version string
    """
    if short:
        return __version__
    return f"DATA ENCRYPTOR/DECRYPTOR v{__version__}"
