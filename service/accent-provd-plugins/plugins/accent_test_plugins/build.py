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


@target('test_plugin', 'test-plugin')
def build_test_plugin(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'test_plugin/', path])


@target('test_plugin_legacy_import', 'test-plugin-legacy-import')
def build_test_plugin_legacy_import(path):
    check_call(['rsync', '-rlp', '--exclude', '.*', 'test_plugin_legacy_import/', path])
