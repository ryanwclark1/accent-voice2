# file: accent_dao/resources/user_call_permission/__init__.py
# Copyright 2025 Accent Communications
"""User call permission resource implementation."""

from .dao import (
    associate,
    dissociate,
    dissociate_all_by_user,
    find_all_by,
    find_by,
    get_by,
)

__all__: list[str] = [
    "associate",
    "dissociate",
    "dissociate_all_by_user",
    "find_all_by",
    "find_by",
    "get_by",
]
