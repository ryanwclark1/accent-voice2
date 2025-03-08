# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

JSON: TypeAlias = Union[str, int, float, bool, None, list['JSON'], dict[str, 'JSON']]
