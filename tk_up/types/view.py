from typing import TypedDict, Any, Literal


class ItemDict(TypedDict):
    text: str
    image: list[str] | Literal[""]  # no idea why it's wrapped in list
    values: list[Any] | Literal[""]
    open: bool  # actually 0 or 1
    tags: list[str] | Literal[""]

class PItemDict(TypedDict):
    parent: str
    text: str
    image: list[str] | Literal[""]  # no idea why it's wrapped in list
    values: list[Any] | Literal[""]
    open: bool  # actually 0 or 1
    tags: list[str] | Literal[""]

class Tag(TypedDict):
    name: str
    bg: str
    fg: str
    image: str
    font: str