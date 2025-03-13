# file: accent_dao/resources/iax_general/init.py # noqa: ERA001
"""Module for initializing the IAX general resources in the accent_dao package.

It imports the `edit_all` and `find_all` functions from the `dao` module and
includes them in the `__all__` list for public access.

Functions:
    edit_all: Function to edit all records.
    find_all: Function to find all records.
"""
# Copyright 2025 Accent Communications

from .dao import edit_all, find_all

__all__: list[str] = ["edit_all", "find_all"]
