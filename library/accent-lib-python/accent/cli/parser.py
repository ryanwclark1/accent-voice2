# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent.cli.commandline import CommandLine
from accent.cli.exception import NoMatchingCommandError

if TYPE_CHECKING:
    from .registry import CommandRegistry


class RawCommandLineParser:
    word_delimiter = ' '

    def __init__(self, command_registry: CommandRegistry) -> None:
        self.command_registry = command_registry

    def split(self, raw_command_line: str) -> list[str]:
        return raw_command_line.split()

    def parse(self, raw_command_line: str) -> CommandLine:
        words = self.split(raw_command_line)
        try:
            command, command_args = self.command_registry.get_command_and_args(words)
        except NoMatchingCommandError:
            command = None
            command_args = None
        return CommandLine(words, command, command_args)
