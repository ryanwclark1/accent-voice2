# Copyright 2023 Accent Communications

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from accent.cli.exception import UsageError

if TYPE_CHECKING:
    from .command.base import BaseCommand
    from .command.unknown import _BaseUnknownCommand
    from .errorhandler import PrintTracebackErrorHandler, ReRaiseErrorHandler
    from .parser import RawCommandLineParser
    from .registry import _NamedCommandDecorator


class Executor:
    def __init__(
        self,
        raw_command_line_source: Iterable[str],
        raw_command_line_parser: RawCommandLineParser,
        error_handler: PrintTracebackErrorHandler | ReRaiseErrorHandler,
        unknown_command_class: type[_BaseUnknownCommand],
    ) -> None:
        self._raw_command_line_source = raw_command_line_source
        self._raw_command_line_parser = raw_command_line_parser
        self._error_handler = error_handler
        self._unknown_command_class = unknown_command_class

    def execute(self) -> None:
        for raw_command_line in self._raw_command_line_source:
            self._process_next_command(raw_command_line)

    def _process_next_command(self, raw_command_line: str) -> None:
        command_line = self._raw_command_line_parser.parse(raw_command_line)
        if command_line.is_blank():
            return

        command: BaseCommand | _NamedCommandDecorator
        if command_line.command is None:
            command = self._unknown_command_class(command_line.words)
        else:
            command = command_line.command

        try:
            execute_args = command.prepare(command_line.command_args)
            command.execute(*execute_args)
        except UsageError:
            print(command.format_usage())  # type: ignore[union-attr]
        except Exception as e:
            self._error_handler.on_exception(e)
