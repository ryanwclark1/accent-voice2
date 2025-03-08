# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .registry import _NamedCommandDecorator


class CommandLine:
    def __init__(
        self,
        words: list[str],
        command: _NamedCommandDecorator | None,
        command_args: list[str] | None,
    ) -> None:
        self.words = words
        self.command = command
        self.command_args = command_args

    def is_blank(self) -> bool:
        return not self.words
