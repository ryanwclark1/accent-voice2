# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypeVar

Self = TypeVar("Self", bound="InputRawCommandLineSource")


class InputRawCommandLineSource:
    def __init__(self, prompt: str) -> None:
        self._prompt = prompt

    def __iter__(self: Self) -> Self:
        return self

    def __next__(self) -> str:
        while True:
            try:
                raw_command_line = input(self._prompt)
                return raw_command_line
            except EOFError:
                print()
                raise StopIteration()
            except KeyboardInterrupt:
                print("^C")

    next = __next__
