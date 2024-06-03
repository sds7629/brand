from datetime import datetime
from typing import Sequence

from pydantic import dataclasses
from app.config import Config


@dataclasses.dataclass
class BaseOrderResponse:
    id: str
    user_id: str
    merchant_id: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    orderer_name: str | None
    phone_num: str | None
    requirements: str | None
    payment_method: str | None
    ordering_date: datetime
    is_payment: bool

@dataclasses.dataclass(config=Config, kw_only=True)
class OrderResponse:
    order_list: Sequence[BaseOrderResponse]
