# Copyright 2025 Accent Communications

"""Accent source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for Accent source operations."""

    resource = "backends/accent/sources"
