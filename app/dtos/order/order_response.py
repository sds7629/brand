from datetime import datetime
from typing import Sequence

from pydantic import dataclasses

from app.config import Config


@dataclasses.dataclass
class PreOrderResponse:
    user_id: str
    email: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    phone_num: str | None
    order_name: str | None
    requirements: str | None
    total_price: int

@dataclasses.dataclass
class CreateOrderResponse:
    order_id: str

# @dataclasses.dataclass
# class OrderItemResponse:
#     name: str
#     price: int
#     image_url: str

@dataclasses.dataclass
class BaseOrderResponse:
    id: str
    address: str
    detail_address: str
    order_name: str
    requirements: str
    ordering_date: datetime
    item: Sequence[str]


@dataclasses.dataclass(config=Config, kw_only=True)
class OrderResponse:
    order_list: Sequence[BaseOrderResponse]
