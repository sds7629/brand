from typing import Sequence

from pydantic import dataclasses

from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class OnlyOneQnAResponse:
    id: str
    title: str
    payload: str
    writer: str
    view_count: int
    is_secret: bool
    is_notice: bool
    image_urls: Sequence[str] | None = None


@dataclasses.dataclass
class QnAResponse:
    qna: Sequence[OnlyOneQnAResponse]
