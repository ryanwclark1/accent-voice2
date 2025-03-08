# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import NoReturn

from accent.cli.command.base import BaseCommand


class ExitCommand(BaseCommand):
    help = 'Exit the interpreter'
    usage = None

    def execute(self) -> NoReturn:
        raise SystemExit()
