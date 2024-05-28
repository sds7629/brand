from datetime import datetime

from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import (
    DeliveryDocument,
    ShowUserDocument,
)


@dataclasses.dataclass
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    ordering_date: datetime
    ordering_request: str
    ordering_item: ItemDocument
    ordering_item_count: int
    zip_code: str
    address: DeliveryDocument
    detail_address: str
    payment_method: str
    total_price: int
    is_fired: bool = False
    is_payment: bool = False
