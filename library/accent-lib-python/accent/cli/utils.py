# Copyright 2023 Accent Communications

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar

from accent.cli.exception import UsageError

R = TypeVar("R")


def compute_ids(command_arg: str) -> list[int]:
    ids = []
    for id_item in command_arg.split(","):
        start, sep, end = id_item.partition("-")
        if not sep:
            ids.append(int(id_item))
        else:
            ids.extend(range(int(start), int(end) + 1))
    return ids


def wraps_error_as_usage_error(fun: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(fun)
    def aux(*args: Any, **kwargs: Any) -> R:
        try:
            return fun(*args, **kwargs)
        except UsageError:
            raise
        except Exception:
            raise UsageError()

    return aux
