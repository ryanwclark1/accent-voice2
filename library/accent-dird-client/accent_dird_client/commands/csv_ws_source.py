# Copyright 2025 Accent Communications

"""CSV web service source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for CSV web service source operations."""

    resource = "backends/csv_ws/sources"
