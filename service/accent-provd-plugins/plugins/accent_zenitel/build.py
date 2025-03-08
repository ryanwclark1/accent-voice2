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


@target('01.11.3.2', 'accent-zenitel-01.11.3.2')
def build_01_11_3_2(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v01_11_3_2/', path])
