# Copyright 2025 Accent Communications

"""Conference source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for conference source operations."""

    resource = "backends/conference/sources"
