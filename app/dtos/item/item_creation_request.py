import dataclasses
from typing import Any, Sequence

from pydantic import HttpUrl

from app.entities.category.category_codes import CategoryCode
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode


@dataclasses.dataclass
class ItemCreationRequest:
    name: str
    price: int
    image_urls: Sequence[HttpUrl]
    description: str
    item_quantity: int
    details: Sequence[str]
    color: ColorCode
    size: SizeCode
    category: CategoryCode
