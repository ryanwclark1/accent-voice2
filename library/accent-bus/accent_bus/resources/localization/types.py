# accent_bus/resources/localization/types.py
# Copyright 2025 Accent Communications

"""Localization types."""

from __future__ import annotations

from typing import TypedDict


class LocalizationDict(TypedDict):
    """Dictionary representing localization settings."""

    country: str
