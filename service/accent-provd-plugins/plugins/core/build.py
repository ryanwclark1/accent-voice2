# Copyright 2023 Accent Communications

# Depends on the following external programs:
#  -rsync

from __future__ import annotations

import os
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


@target('null', 'null', std_dirs=False)
def build_null(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'null/', path])


@target('zero', 'zero', std_dirs=False)
def build_zero(path: str) -> None:
    os.makedirs(os.path.join(path, 'var/tftpboot'))
    check_call(['rsync', '-rlp', '--exclude', '.*', 'zero/', path])
