# accent_bus/resources/common/acl.py
# Copyright 2025 Accent Communications

"""ACL utility functions."""


def escape(acl_part: str) -> str:
    """Escape an ACL part.

    Args:
       acl_part (str):  ACL part to escape.

    Returns:
        str: The escaped ACL part.

    """
    return (
        acl_part.replace(".", "__DOT__")
        .replace("#", "__HASH__")
        .replace("*", "__STAR__")
    )
