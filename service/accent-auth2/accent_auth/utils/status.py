# accent_auth/utils/status.py
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    StatusDict = defaultdict[str, defaultdict[str, str]]
    StatusProvider = Callable[[StatusDict], None]


class Status:
    fail = "fail"
    ok = "ok"


class StatusAggregator:
    def __init__(self) -> None:
        self._providers: list[StatusProvider] = []

    def add_provider(self, status_provider: StatusProvider) -> None:
        self._providers.append(status_provider)

    def status(self) -> StatusDict:
        status = _default_dict()
        for provider in self._providers:
            provider(status)
        return status


def _default_dict() -> defaultdict[str, defaultdict]:
    return defaultdict(_default_dict)
