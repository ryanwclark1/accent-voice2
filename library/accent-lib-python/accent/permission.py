# Copyright 2023 Accent Communications

from __future__ import annotations


def escape(acl_part: str) -> str:
    return (
        acl_part.replace(".", "__DOT__")
        .replace("#", "__HASH__")
        .replace("*", "__STAR__")
    )
