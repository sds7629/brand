import dataclasses
from datetime import datetime
from typing import Sequence

from app.dtos.item.item_creation_request import FitSizing, ItemOptions
from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class ItemUpdateRequest:
    name: str | None = None
    price: int | None = None
    description: str | None = None
    details: Sequence[str] | None = None
    fit_sizing: FitSizing | None = None
    fabric: str | None = None
    options: Sequence[ItemOptions] | None = None
    category: CategoryCode | None = None
    updated_at: datetime = datetime.utcnow()
