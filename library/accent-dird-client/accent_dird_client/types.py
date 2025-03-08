# Copyright 2023 Accent Communications
from __future__ import annotations

from typing import TypeAlias, Union

JSON: TypeAlias = Union[str, int, float, bool, None, list['JSON'], dict[str, 'JSON']]
