# file: accent_dao/resources/voicemail_zonemessages/__init__.py
# Copyright 2025 Accent Communications
"""Voicemail zonemessages settings resource implementation."""

from .dao import (
    async_edit_all,
    async_find_all,
)

__all__: list[str] = [
    "async_edit_all",
    "async_find_all",
]
