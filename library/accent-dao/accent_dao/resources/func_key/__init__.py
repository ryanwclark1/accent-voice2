# file: accent_dao/resources/func_key/__init__.py
# Copyright 2025 Accent Communications
"""Function key resource implementation and related functionalities."""

from . import dao, hint_dao, type_dao

__all__: list[str] = [
    "dao",
    "hint_dao",
    "type_dao",
]
