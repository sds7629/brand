from typing import Sequence

from pydantic import HttpUrl, dataclasses


@dataclasses.dataclass
class CartItemResponse:
    item_id: str
    item_name: str
    image_urls: Sequence[HttpUrl]


@dataclasses.dataclass
class CartResponse:
    cart_id: str
    item: CartItemResponse
    quantity: int
    options: str
    total_price: int


@dataclasses.dataclass
class CartCreationResponse:
    cart_id: Sequence[str]
