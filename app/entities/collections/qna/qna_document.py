from datetime import datetime
from typing import Optional, Annotated

from pydantic import  dataclasses, AfterValidator, HttpUrl
from pydantic.dataclasses import Field

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument

#Url 유효성 검증
HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]

@dataclasses.dataclass
class ReplyDocument(BaseDocument):
    writer: ShowUserDocument
    payload: str
    image_url: HttpUrlString | None
    updated_at: Optional[datetime] = None


@dataclasses.dataclass
class QnADocument(BaseDocument):
    title: str
    payload: str
    qna_password: str | None
    writer: ShowUserDocument
    image_url: HttpUrlString | None
    reply: list[ReplyDocument] | None = Field(default_factory=list)
    updated_at: Optional[datetime] = None

