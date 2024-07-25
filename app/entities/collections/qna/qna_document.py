from datetime import datetime
from typing import Annotated, Optional, Sequence

from pydantic import AfterValidator, HttpUrl, dataclasses
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument

HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]


@dataclasses.dataclass
class QnADocument(BaseDocument):
    title: str
    payload: str
    writer: ShowUserDocument
    image_urls: Sequence[HttpUrlString] | None
    view_count: int
    is_secret: bool
    is_notice: bool
    updated_at: Optional[datetime] = None
