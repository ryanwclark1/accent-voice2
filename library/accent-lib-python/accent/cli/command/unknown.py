# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import NoReturn

from accent.cli.command.base import BaseCommand


class _BaseUnknownCommand(BaseCommand):
    help = 'Handler for unknown commands'
    usage = None
    _error_msg = None

    def __init__(self, words: list[str]) -> None:
        self._error_msg = f'no such command: {words[0]}'


class PrintingUnknownCommand(_BaseUnknownCommand):
    def execute(self) -> None:
        print(self._error_msg)


class RaisingUnknownCommand(_BaseUnknownCommand):
    def execute(self) -> NoReturn:
        raise Exception(self._error_msg)
