from typing import Sequence

from pydantic import HttpUrl, dataclasses


@dataclasses.dataclass
class CartItemResponse:
    item_id: str
    item_name: str
    image_urls: Sequence[HttpUrl]
    size: str
    color: str


@dataclasses.dataclass
class CartResponse:
    cart_id: str
    item: CartItemResponse
    quantity: int
    total_price: int


@dataclasses.dataclass
class CartCreationResponse:
    cart_id: Sequence[str]
