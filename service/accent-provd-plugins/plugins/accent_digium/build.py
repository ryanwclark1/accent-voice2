# Copyright 2023 Accent Communications

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


@target('1.4.0.0', 'accent-digium-1.4.0.0')
def build_1_4_0_0(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v1_4_0_0/', path])


@target('2.2.1.8', 'accent-digium-2.2.1.8')
def build_2_2_1_8(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v2_2_1_8/', path])


@target('2.8.1', 'accent-digium-2.8.1')
def build_2_8_1(path: str) -> None:
    check_call(['rsync', '-rlp', '--exclude', '.*', 'common/', path])
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v2_8_1/', path])
