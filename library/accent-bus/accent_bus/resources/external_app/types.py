# resources/external_app/types.py
from typing import TypedDict


class ExternalAppDict(TypedDict, total=False):
    """Represents an external application."""

    name: str
