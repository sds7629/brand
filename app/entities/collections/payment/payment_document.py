from datetime import datetime

from pydantic import dataclasses

from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass

class PaymentDocument:
    user: ShowUserDocument
    order: OrderDocument
    item: ItemDocument
    item_option: str
    total_price: int
    payment_time: datetime
    is_reviewed: bool

