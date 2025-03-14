# Copyright 2023 Accent Communications

"""System functions

Copyright (C) 2008-2010  Avencall

WARNING: Linux specific module - and maybe even Debian specific module
"""

from __future__ import annotations

__version__ = "$Revision$ $Date$"

import logging
import os
import shutil
import subprocess
from collections.abc import Sequence
from typing import TextIO

log = logging.getLogger("accent.system")


def sync_no_oserror() -> None:
    """
    Call /bin/sync.
    Catch and log OSError exceptions.
    """
    try:
        subprocess.call("/bin/sync", close_fds=True)
    except OSError:
        log.warning("sync_no_oserror: call of /bin/sync failed", exc_info=True)


def rm_rf(path: str) -> None:
    """
    Recursively (if needed) delete path.
    """
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.lexists(path):
        os.remove(path)


def flush_sync_file_object(fo: TextIO) -> None:
    """
    Flush internal buffers of @fo, then ask the OS to flush its own buffers.
    """
    fo.flush()
    os.fsync(fo.fileno())


def file_writelines_flush_sync(path: str, lines: Sequence[str]) -> None:
    """
    Fill file at @path with @lines then flush all buffers
    (Python and system buffers)
    """
    with open(path, "w") as fp:
        fp.writelines(lines)
        flush_sync_file_object(fp)


def file_w_create_directories(filepath: str) -> TextIO:
    """
    Recursively create some directories if needed so that the directory where
    @filepath must be written exists, then open it in "w" mode and return the
    file object.
    """
    dirname = os.path.dirname(filepath)
    if dirname and dirname != os.path.curdir and not os.path.isdir(dirname):
        os.makedirs(dirname)
    return open(filepath, "w")
