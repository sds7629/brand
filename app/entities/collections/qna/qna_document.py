import dataclasses
import datetime
from dataclasses import field

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import UserDocument


@dataclasses.dataclass
class QnADocument(BaseDocument):
    title: str
    payload: str
    image_url: str
    qna_password: str
    updated_at: datetime.time() | None
    writer: list[UserDocument]
