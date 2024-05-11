import dataclasses

from typing import Sequence, Any

from pydantic import BaseModel

from app.entities.collections.users.user_document import ShowUserDocument



class BeforeQnAResponse(BaseModel):
    id: str
    title: str
    payload: str
    writer: [ShowUserDocument]
    image_url: str | None = None

@dataclasses.dataclass
class QnAResponse:
    qna: Sequence[BeforeQnAResponse]
