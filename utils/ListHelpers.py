from __future__ import annotations
from typing import List, TypeVar

T = TypeVar('T')


def get_by_index(source: List[T], idx: int, default: T = None) -> T:
    try:
        return source[idx]
    except IndexError:
        return default
