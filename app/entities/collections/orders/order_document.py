from datetime import datetime
from typing import Sequence

from pydantic import dataclasses

from app.config import Config
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass(config=Config)
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    email: str
    merchant_id: str
    post_code: str
    address: str
    detail_address: str
    requirements: str
    order_name: str
    phone_num: str
    payment_method: str
    total_price: int
    ordering_item: Sequence[ItemDocument]
    ordering_date: datetime
    is_payment: bool


@dataclasses.dataclass
class PreOrderDocument:
    user: ShowUserDocument
    email: str | None
    merchant_id: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    requirements: str | None
    order_name: str | None
    phone_num: str | None
    payment_method: str | None
    total_price: int
    is_payment: bool
