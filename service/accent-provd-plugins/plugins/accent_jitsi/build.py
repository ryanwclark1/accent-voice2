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


@target('1', 'accent-jitsi-1')
def build_1(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1/', path])
