import dataclasses
from datetime import datetime

from app.entities.category.category_codes import CategoryCode
from pydantic import HttpUrl

@dataclasses.dataclass
class ItemCreationRequest:
    name: str
    price: int
    image_url: HttpUrl
    description: str
    registration_date: datetime
    item_quantity: int
    size: str
    category: list[CategoryCode]
