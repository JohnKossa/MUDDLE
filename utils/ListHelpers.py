from __future__ import annotations
from typing import Optional, TypeVar

T = TypeVar('T')


def get_by_index(source: list[T], idx: int, default: T = None) -> Optional[T]:
    try:
        return source[idx]
    except IndexError:
        return default
