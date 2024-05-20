from datetime import datetime
from typing import Sequence

from pydantic import dataclasses

from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class OneItemResponse:
    id: str
    name: str
    price: int
    image_url: str
    description: str
    registration_date: datetime
    item_quantity: int
    size: str
    category_codes: list[CategoryCode]


@dataclasses.dataclass
class ItemResponse:
    item: Sequence[OneItemResponse]
