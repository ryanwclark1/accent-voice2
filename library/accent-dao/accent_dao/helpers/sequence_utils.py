
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar('T')

Predicate = Callable[[T], bool]


def split_by(seq: Iterable[T], pred: Predicate[T]) -> tuple[list[T], list[T]]:
    approved = []
    rejected = []
    for x in seq:
        if pred(x):
            approved.append(x)
        else:
            rejected.append(x)

    return approved, rejected
