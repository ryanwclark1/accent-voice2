# helpers/uuid.py
# Copyright 2025 Accent Communications

from uuid import uuid4


def new_uuid() -> str:
    """Generate a new UUID as a string.

    Returns:
        str: A random UUID in string format.

    """
    return str(uuid4())
