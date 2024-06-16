from typing import Sequence

from pydantic import dataclasses

from app.config import Config
from app.utils.enums.payment_codes import PaymentMethodCode


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
    payment_method: PaymentMethodCode
    total_price: int
    cart_id: Sequence[str]
