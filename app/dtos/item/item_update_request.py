import dataclasses
from datetime import datetime
from typing import Sequence

from pydantic import HttpUrl

from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class ItemUpdateRequest:
    name: str | None = None
    price: int | None = None
    description: str | None = None
    item_quantity: int | None = None
    size: str | None = None
    category: list[CategoryCode] | None = None
    updated_at: datetime = datetime.utcnow()
