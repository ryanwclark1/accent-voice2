# Copyright 2023 Accent Communications

from __future__ import annotations

import re

COMPLETE_CALLER_ID_PATTERN = re.compile(r"\"(.*)\" \<(\+?\d+)\>")


def is_complete_caller_id(caller_id: str) -> bool:
    return bool(COMPLETE_CALLER_ID_PATTERN.match(caller_id))


def extract_number(caller_id: str) -> str:
    if match := COMPLETE_CALLER_ID_PATTERN.search(caller_id):
        return match.groups()[1]
    raise ValueError("Not a valid Caller ID: %s", caller_id)


def extract_displayname(caller_id: str) -> str:
    if match := COMPLETE_CALLER_ID_PATTERN.search(caller_id):
        return match.groups()[0]
    raise ValueError("Not a valid Caller ID: %s", caller_id)


def assemble_caller_id(fullname: str, number: str | None) -> str:
    if number:
        return f'"{fullname}" <{number}>'
    return f'"{fullname}"'
