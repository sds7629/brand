from typing import Sequence, Any

from pydantic import dataclasses

from app.config import Config
from app.utils.enums.payment_codes import PaymentMethodCode


@dataclasses.dataclass(config=Config)
class PreOrderCreationRequest:
    options: str
    item_id: str | None = None
    cart_id: str | None = None


@dataclasses.dataclass(config=Config)
class OrderCreationRequest:
    item_id: str
    merchant_id: str
    post_code: str
    address: str
    detail_address: str
    phone_num: str
    order_name: str
    requirements: str | None
    payment_method: PaymentMethodCode
    total_price: int
