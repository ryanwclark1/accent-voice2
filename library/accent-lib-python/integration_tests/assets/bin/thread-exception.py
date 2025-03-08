#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from __future__ import annotations

import threading
import time
from typing import NoReturn

from accent import accent_logging

accent_logging.setup_logging("/dev/null")


def failure() -> NoReturn:
    raise RuntimeError("If you see this, then the exception is logged!")


threading.Thread(target=failure).start()

while True:
    time.sleep(1)
