# file: accent_dao/resources/voicemail_general/__init__.py
# Copyright 2025 Accent Communications
"""Voicemail general settings resource implementation."""

from .dao import (
    edit_all,
    find_all,
)

__all__: list[str] = [
    "edit_all",
    "find_all",
]
