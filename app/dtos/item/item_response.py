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
    options: dict[str, int]
    item_details_menu: dict[str, Any]
    registration_date: datetime
    category_codes: CategoryCode


@dataclasses.dataclass
class ItemResponse:
    item: Sequence[OneItemResponse]
    page_count: int
