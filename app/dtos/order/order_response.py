from datetime import datetime
from typing import Sequence

from pydantic import dataclasses
from app.config import Config
from app.dtos.item.item_response import OneItemResponse
from app.entities.collections.users.user_document import DeliveryDocument


@dataclasses.dataclass
class BaseOrderResponse:
    id: str
    ordering_date: datetime
    ordering_request: str
    ordering_item: OneItemResponse
    ordering_item_mount: int
    post_code: str
    address: DeliveryDocument
    detail_address: str
    payment_method: str
    total_price: int
    merchant_uid: str


@dataclasses.dataclass(config=Config, kw_only=True)
class OrderResponse:
    order_list: Sequence[BaseOrderResponse]
