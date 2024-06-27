from datetime import datetime
from typing import Any, Sequence

from pydantic import HttpUrl, dataclasses

from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class OneItemResponse:
    id: str
    name: str
    price: int
    image_urls: Sequence[HttpUrl]
    description: str
    registration_date: datetime
    item_quantity: int
    size: str
    color: str
    category_codes: CategoryCode
    details: Sequence[str] | None = None


@dataclasses.dataclass
class ItemResponse:
    item: Sequence[OneItemResponse]
    page_count: int
