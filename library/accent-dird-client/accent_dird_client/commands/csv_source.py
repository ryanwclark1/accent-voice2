# Copyright 2025 Accent Communications

"""CSV source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for CSV source operations."""

    resource = "backends/csv/sources"
