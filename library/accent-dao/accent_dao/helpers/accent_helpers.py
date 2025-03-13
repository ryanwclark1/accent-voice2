from __future__ import annotations

import re

find_asterisk_pattern_char = re.compile(r"[\[NXZ!.]").search


def position_of_asterisk_pattern_char(ast_pattern: str) -> int | None:
    """Find the position of the first asterisk pattern character in the given string.

    Args:
        ast_pattern (str): The string to search for the asterisk pattern character.

    Returns:
        int | None: The position of the first asterisk pattern character
            if found, otherwise None.

    """
    if not (mo := find_asterisk_pattern_char(ast_pattern)):
        return None
    return mo.start()


def clean_extension(exten: str | None) -> str:
    """Return an extension from an Asterisk extension pattern."""
    if exten is None:
        return ""

    exten = str(exten)

    if exten.startswith("_"):
        exten = exten[1:]
        e = position_of_asterisk_pattern_char(exten)
        if e is not None:
            exten = exten[:e]

    return exten
