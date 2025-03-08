# Copyright 2023 Accent Communications

from accent_dird_client.commands.helpers.base_source_command import SourceCommand


class Command(SourceCommand):
    resource = 'backends/csv_ws/sources'
