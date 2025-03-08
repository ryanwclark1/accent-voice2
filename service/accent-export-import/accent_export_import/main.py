# Copyright 2023 Accent Communications

import logging
import sys

from .dump import AccentGenerateDump
from .import_ import AccentImportDump

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s (%(levelname)s) (%(name)s): %(message)s",
)

logger = logging.getLogger("pyexcel_io")
logger.setLevel(logging.ERROR)


def dump(argv=None):
    argv = argv or sys.argv[1:]
    app = AccentGenerateDump()
    return app.run(argv)


def import_(argv=None):
    argv = argv or sys.argv[1:]
    app = AccentImportDump()
    return app.run(argv)
