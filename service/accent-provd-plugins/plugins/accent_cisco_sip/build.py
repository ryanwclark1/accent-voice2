# Copyright 2023 Accent Communications

# Depends on the following external programs:
#  -rsync

from __future__ import annotations

from collections.abc import Callable
from subprocess import check_call
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    def target(
        target_id: str, plugin_id: str, std_dirs: bool = True
    ) -> Callable[[Callable[[str], None]], None]:
        """The `target` method is injected in `exec` call by the build script."""

        def wrapper(func: Callable[[str], None]) -> None:
            pass

        return wrapper


@target('9.3', 'accent-cisco-sip-9.3')
def build_9_3(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v9_3/', path])


@target('11.1.0', 'accent-cisco-sip-11.1.0')
def build_11_1_0(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v11_1_0/', path])


@target('11.3.1', 'accent-cisco-sip-11.3.1')
def build_11_3_1(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v11_3_1/', path])


@target('12.0.1', 'accent-cisco-sip-12.0.1')
def build_12_0_1(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v12_0_1/', path])
