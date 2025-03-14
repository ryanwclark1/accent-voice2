# resources/common/routing_key.py
def escape(routing_key_part: str) -> str:
    """Escapes special characters in a routing key part.

    Args:
        routing_key_part: The routing key part to escape.

    Returns:
        The escaped routing key part.

    """
    return (
        routing_key_part.replace(".", "__DOT__")
        .replace("#", "__HASH__")
        .replace("*", "__STAR__")
    )
