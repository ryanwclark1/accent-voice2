# Copyright 2025 Accent Communications

"""Phonebook source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for phonebook source operations."""

    resource = "backends/phonebook/sources"
