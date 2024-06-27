import dataclasses
from typing import Sequence


@dataclasses.dataclass
class QnARequest:
    title: str
    payload: str
    is_secret: bool
    image_urls: Sequence[str] | None = None


@dataclasses.dataclass
class UpdateQnARequest:
    title: str | None
    payload: str | None
    image_urls: Sequence[str] | None
