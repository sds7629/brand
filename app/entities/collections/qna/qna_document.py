import dataclasses
import datetime
from dataclasses import field

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class QnADocument(BaseDocument):
    title: str
    payload: str
    qna_password: str | None
    writer: ShowUserDocument
    image_url: str | None
    updated_at: datetime.time() = None
