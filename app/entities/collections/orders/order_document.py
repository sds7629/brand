from datetime import datetime
from typing import Sequence

from pydantic import dataclasses

from app.config import Config
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.enums.payment_codes import PaymentMethodCode
from app.utils.enums.status_codes import StatusCode


@dataclasses.dataclass(config=Config)
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    order_name: str
    merchant_id: str
    post_code: str
    address: str
    detail_address: str
    requirements: str
    phone_num: str
    payment_status: StatusCode
    payment_method: PaymentMethodCode
    total_price: int
    item_name: str
    is_payment: bool


@dataclasses.dataclass
class PreOrderDocument:
    user: ShowUserDocument
    order_name: str | None
    merchant_id: str | None
    post_code: str | None
    address: str
    detail_address: str
    requirements: str
    phone_num: str | None
    payment_status: StatusCode | None
    payment_method: PaymentMethodCode | None
    total_price: int
    ordering_item: Sequence[ItemDocument]
