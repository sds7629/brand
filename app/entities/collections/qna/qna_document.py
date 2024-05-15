from pydantic import dataclasses,AwareDatetime

from typing import Optional

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class ApplyDocument(BaseDocument):
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
    apply: list[ApplyDocument] | None
    updated_at: Optional[AwareDatetime] = None
