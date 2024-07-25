from datetime import datetime
from typing import Sequence

from pydantic import HttpUrl, dataclasses

from app.config import Config


@dataclasses.dataclass
class OrderItemResponse:
    item_id: str
    option: str
    quantity: int


@dataclasses.dataclass
class PreOrderResponse:
    user_id: str
    merchant_id: str | None
    email: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    recipient_name: str
    phone_num: str | None
    requirements: str | None
    total_price: int
    ordering_item: Sequence[OrderItemResponse]


@dataclasses.dataclass
class CreateOrderResponse:
    order_id: str


@dataclasses.dataclass
class BaseOrderResponse:
    id: str
    merchant_id: str
    address: str
    detail_address: str
    recipient_name: str
    requirements: str
    ordering_date: datetime
    items: Sequence[OrderItemResponse]


@dataclasses.dataclass(config=Config, kw_only=True)
class OrderResponse:
    order_list: Sequence[BaseOrderResponse]
