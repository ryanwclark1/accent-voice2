# Copyright 2023 Accent Communications

from __future__ import annotations

import os
from typing import Any

from accent_amid.ami.parser import parse_buffer

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def pass_(*args: Any, **kwargs: Any) -> None:
    pass


with open(os.path.join(__location__, 'ami-messages.txt'), 'rb') as f:
    sample = f.read().replace(b'\n', b'\r\n')

ami_stream = sample * 50

parse_buffer(ami_stream, pass_, pass_)
