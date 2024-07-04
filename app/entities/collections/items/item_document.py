from datetime import datetime
from typing import Annotated, Any, Sequence

from pydantic import AfterValidator, HttpUrl, dataclasses

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.base_document import BaseDocument


HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]


@dataclasses.dataclass
class ItemDocument(BaseDocument):
    name: str
    price: int
    image_urls: Sequence[HttpUrlString]
    description: str
    registration_date: datetime
    options: dict[str, int]
    item_detail_menu: dict[str, Any]
    category_codes: CategoryCode
    updated_at: datetime | None = None
    is_deleted: bool = False
