from typing import Sequence

from pydantic import dataclasses

from app.config import Config


@dataclasses.dataclass(config=Config)
class PreOrderCreationRequest:
    cart_id: Sequence[str]


@dataclasses.dataclass(config=Config)
class OrderCreationRequest:
    email: str
    post_code: str
    address: str
    detail_address: str
    phone_num: str
    order_name: str
    requirements: str | None
    payment_method: str
    total_price: int
    cart_id: Sequence[str]