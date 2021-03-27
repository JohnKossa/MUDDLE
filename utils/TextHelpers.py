from __future__ import annotations
from typing import List


def enumerate_objects(items: List[str]) -> str:
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    if len(items) > 2:
        return (", ".join(items[:-1]))+f", and {items[-1]}"
    raise Exception("Call to TextHelpers.enumerate_objects contained less than 1 item.")


def pluralize(item: str, count: int) -> str:
    if count == 1:
        return item
    if count == 0 or count > 1:
        return f"{item}s"
    raise Exception("Call to TextHelpers had less than 0 count")
