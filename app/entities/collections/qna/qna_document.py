from typing import Optional

from pydantic import AwareDatetime, dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class ReplyDocument(BaseDocument):
    writer: ShowUserDocument
    payload: str
    image_url: str
    updated_at: Optional[AwareDatetime] = None


@dataclasses.dataclass
class QnADocument(BaseDocument):
    title: str
    payload: str
    qna_password: str | None
    writer: ShowUserDocument
    image_url: str | None
    reply: list[ReplyDocument] | None = None
    updated_at: Optional[AwareDatetime] = None
