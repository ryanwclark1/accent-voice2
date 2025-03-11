# Copyright 2025 Accent Communications

"""LDAP source command implementation."""

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    """Command for LDAP source operations."""

    resource = "backends/ldap/sources"
