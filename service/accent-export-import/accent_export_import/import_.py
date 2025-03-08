# Copyright 2023 Accent Communications

from cliff import app, commandmanager


class AccentImportDump(app.App):
    def __init__(self):
        super().__init__(
            description="Dump file importer for Accent",
            command_manager=commandmanager.CommandManager("accent_export_import.import_commands"),
            version="1.0.0",
        )
