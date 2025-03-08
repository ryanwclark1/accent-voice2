# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any, NoReturn


class BaseCommand:
    help: str
    usage: str | None

    def prepare(self, command_args: list[str] | None) -> tuple[Any, ...]:
        return ()

    def execute(self, *args: Any, **kwargs: Any) -> NoReturn | None:
        # must be overriden in derived class
        raise NotImplementedError()
