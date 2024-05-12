from typing import Sequence

from pydantic import dataclasses

from app.config import Config
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class OnlyOneQnAResponse:
    id: str
    title: str
    payload: str
    writer: ShowUserDocument
    image_url: str | None = None


@dataclasses.dataclass
class QnAResponse:
    qna: Sequence[OnlyOneQnAResponse]
