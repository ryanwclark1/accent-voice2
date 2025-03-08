# Copyright 2023 Accent Communications

from cliff import app, commandmanager


class AccentGenerateDump(app.App):
    def __init__(self):
        super().__init__(
            description="A dump file builder for Accent",
            command_manager=commandmanager.CommandManager("accent_export_import.dump_commands"),
            version="1.0.0",
        )
