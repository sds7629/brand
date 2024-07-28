from datetime import datetime
from typing import Optional

from pydantic import dataclasses
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class NoticeDocument(BaseDocument):
    title: str
    payload: str
    writer: ShowUserDocument
    updated_at: Optional[datetime]
