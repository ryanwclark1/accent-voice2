# accent_bus/resources/common/routing_key.py
# Copyright 2025 Accent Communications

"""Routing key utility functions."""


def escape(routing_key_part: str) -> str:
    """Escape a routing key part.

    Args:
       routing_key_part (str): The routing key part to escape.

    Returns:
        str: The escaped routing key part.

    """
    return (
        routing_key_part.replace(".", "__DOT__")
        .replace("#", "__HASH__")
        .replace("*", "__STAR__")
    )
