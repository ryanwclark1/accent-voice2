"""
Copyright 2023 Accent Communications
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 -rsync
"""
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


@target('2.3', 'accent-fanvil-2.3')
def build_2_3(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v2_3/', path])


@target('serie-x', 'accent-fanvil-serie-x')
def build_x(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie_x/', path])


@target('serie-v', 'accent-fanvil-serie-v')
def build_v(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie_v/', path])


@target('serie-i', 'accent-fanvil-serie-i')
def build_i(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie_i/', path])


@target('serie-h', 'accent-fanvil-serie-h')
def build_h(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'serie_h/', path])
