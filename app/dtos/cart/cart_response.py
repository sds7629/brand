from typing import Sequence

from pydantic import dataclasses, HttpUrl


@dataclasses.dataclass
class CartItemResponse:
    item_id: str
    item_name: str
    image_url: HttpUrl
    size: str
    color: str
    price: int

@dataclasses.dataclass
class CartResponse:
    cart_id: str
    items: Sequence[CartItemResponse]
    mount: int
    total_price: int