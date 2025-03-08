# Copyright 2023 Accent Communications

from __future__ import annotations

import traceback
from typing import NoReturn


class ReRaiseErrorHandler:
    def on_exception(self, e: Exception) -> NoReturn:
        raise


class PrintTracebackErrorHandler:
    def on_exception(self, e: Exception) -> None:
        traceback.print_exc()
