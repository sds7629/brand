import dataclasses
from typing import Any, Sequence

from app.entities.category.category_codes import CategoryCode
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode


@dataclasses.dataclass
class ItemOptions:
    color_size: str
    quantity: int


@dataclasses.dataclass
class FitSizing:
    model_fit: str
    item_size: str


@dataclasses.dataclass
class ItemCreationRequest:
    name: str
    price: int
    description: str
    details: Sequence[str]
    fit_sizing: FitSizing
    fabric: str
    options: Sequence[ItemOptions]
    category: CategoryCode
