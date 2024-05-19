from datetime import datetime

from pydantic import dataclasses, HttpUrl, AfterValidator
from app.entities.category.category_codes import CategoryCode
from typing import Annotated

from app.entities.collections.base_document import BaseDocument

HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]

@dataclasses.dataclass
class ItemDocument(BaseDocument):
    name: str
    price: int
    image_url: HttpUrlString
    description: str
    registration_date: datetime
    item_quantity: int
    size: str
    category_codes: list[CategoryCode]
    updated_at: datetime | None = None
    is_deleted: bool = False
