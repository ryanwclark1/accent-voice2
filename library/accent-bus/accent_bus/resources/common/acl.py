# resources/common/acl.py
def escape(acl_part: str) -> str:
    """Escapes special characters in an ACL part.

    Args:
        acl_part: The ACL part to escape.

    Returns:
        The escaped ACL part.

    """
    return (
        acl_part.replace(".", "__DOT__")
        .replace("#", "__HASH__")
        .replace("*", "__STAR__")
    )
