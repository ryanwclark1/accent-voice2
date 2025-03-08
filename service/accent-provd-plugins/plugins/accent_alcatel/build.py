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


@target('2.01.10', 'accent-alcatel-2.01.10')
def build_2_01_10(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v2_01_10/', path])


@target('2.13.02', 'accent-alcatel-2.13.02')
def build_2_13_02(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v2_13_02/', path])


@target('1.51.52', 'accent-alcatel-1.51.52')
def build_1_51_52(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_51_52/', path])
