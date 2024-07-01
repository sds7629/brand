import dataclasses
from typing import Sequence


@dataclasses.dataclass
class QnARequest:
    title: str
    payload: str
    is_secret: bool


@dataclasses.dataclass
class UpdateQnARequest:
    title: str | None = None
    payload: str | None = None
    is_secret: bool | None = None
