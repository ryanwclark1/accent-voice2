# helpers/sequence_utils.py
# Copyright 2025 Accent Communications

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")

Predicate = Callable[[T], bool]


def split_by(seq: Iterable[T], pred: Predicate[T]) -> tuple[list[T], list[T]]:
    """Split a sequence into two lists based on a predicate.

    Args:
        seq: The iterable sequence to split.
        pred: A predicate function that returns True for items to include
              in the approved list and False for the rejected list.

    Returns:
        A tuple containing two lists:
            - The first list contains all items for which the predicate returns True.
            - The second list contains all items for which the predicate returns False.

    """
    approved = []
    rejected = []
    for x in seq:
        if pred(x):
            approved.append(x)
        else:
            rejected.append(x)

    return approved, rejected
