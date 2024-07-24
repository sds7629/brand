from datetime import datetime
from typing import Any, Sequence

from bson import ObjectId
from pydantic import dataclasses

from app.config import Config
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.enums.status_codes import StatusCode


@dataclasses.dataclass
class OrderItem:
    item: ItemDocument
    option: str
    quantity: int


@dataclasses.dataclass(config=Config)
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    order_item: Sequence[OrderItem]
    recipient_name: str
    merchant_id: str
    post_code: str
    address: str
    detail_address: str
    requirements: str
    phone_num: str
    payment_status: StatusCode
    total_price: int
    is_payment: bool


@dataclasses.dataclass
class PreOrderDocument:
    user: ShowUserDocument
    merchant_id: str | None
    email: str | None
    recipient_name: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    requirements: str | None
    phone_num: str | None
    total_price: int
    ordering_item: Sequence[dict[str, Any]]
