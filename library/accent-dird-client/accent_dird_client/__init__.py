# Copyright 2025 Accent Communications

"""Accent Directory Client for API interactions.

This package provides a client for interacting with the Accent Directory Service API,
supporting both synchronous and asynchronous operations.
"""

from accent_dird_client.client import DirdClient as Client
from accent_dird_client.models import (
    ContactModel,
    DirectoryModel,
    PhonebookModel,
    ProfileModel,
    SourceModel,
)

__all__ = [
    "Client",
    "ContactModel",
    "DirectoryModel",
    "PhonebookModel",
    "ProfileModel",
    "SourceModel",
]
