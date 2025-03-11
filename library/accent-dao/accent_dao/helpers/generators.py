# helpers/generators.py
# Copyright 2025 Accent Communications

import random
import string
from collections.abc import Callable
from typing import TypeVar

# Type definitions
T = TypeVar("T")

# Constants
ALPHANUMERIC_POOL = string.ascii_lowercase + string.digits


def find_unused_hash(already_exists_predicate: Callable[[str], bool]) -> str:
    """Find a hash that doesn't exist according to the provided predicate.

    This function continuously generates random hashes until it finds one
    that satisfies the condition defined by the already_exists_predicate.

    Args:
        already_exists_predicate: A function that returns True if the hash already exists.

    Returns:
        str: A unique hash that doesn't already exist.

    """
    while True:
        data = generate_hash()
        if not already_exists_predicate(data):
            return data


def generate_hash(length: int = 8) -> str:
    """Generate a random alphanumeric hash of the specified length.

    Args:
        length: The length of the hash to generate. Defaults to 8.

    Returns:
        str: A random alphanumeric hash.

    """
    return "".join(random.choice(ALPHANUMERIC_POOL) for _ in range(length))
