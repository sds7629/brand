from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, HttpUrl, dataclasses

from app.entities.category.category_codes import CategoryCode
from app.utils.enums.size_codes import SizeCode
from app.utils.enums.color_codes import ColorCode
from app.entities.collections.base_document import BaseDocument

HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]


@dataclasses.dataclass
class ItemDocument(BaseDocument):
    name: str
    color: ColorCode
    price: int
    image_url: HttpUrlString
    description: str
    registration_date: datetime
    item_quantity: int
    size: SizeCode
    category_codes: list[CategoryCode]
    updated_at: datetime | None = None
    is_deleted: bool = False
