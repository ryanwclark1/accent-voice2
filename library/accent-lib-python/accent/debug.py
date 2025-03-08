# Copyright 2023 Accent Communications

from __future__ import annotations

import functools
import logging
import os
import time
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

DEBUG_MODE = os.environ.get("ACCENT_DEBUG")


F = TypeVar("F", bound=Callable[..., Any])
R = TypeVar("R")


def _debug(decorator: Callable[[F], F]) -> F | Callable[[F], F]:
    if DEBUG_MODE:
        return decorator
    return _no_op_decorator


def _no_op_decorator(fun: F) -> F:
    return fun


@_debug
def trace_duration(fun: Callable[..., R]) -> Callable[..., R]:
    fun_name = fun.__name__

    @functools.wraps(fun)
    def aux(*args: Any, **kwargs: Any) -> R:
        start_time = time.time()
        result = fun(*args, **kwargs)
        duration = time.time() - start_time
        logger.info("Execution of %r took %.3fs", fun_name, duration)
        return result

    return aux


@_debug
def trace_call(fun: Callable[..., R]) -> Callable[..., R]:
    fun_name = fun.__name__

    @functools.wraps(fun)
    def aux(*args: Any, **kwargs: Any) -> R:
        logger.info("Executing %r", fun_name)
        result = fun(*args, **kwargs)
        return result

    return aux
