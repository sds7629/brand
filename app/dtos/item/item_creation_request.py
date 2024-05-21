import dataclasses

from pydantic import HttpUrl

from app.entities.category.category_codes import CategoryCode


@dataclasses.dataclass
class ItemCreationRequest:
    name: str
    price: int
    image_url: HttpUrl
    description: str
    item_quantity: int
    size: str
    category: list[CategoryCode]
