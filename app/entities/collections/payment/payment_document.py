from datetime import datetime
from typing import Sequence

from bson import ObjectId
from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class PaymentDocument(BaseDocument):
    user: ShowUserDocument
    order: ObjectId
    items: Sequence[ItemDocument]
    total_price: int
    payment_time: datetime
    is_reviewed: bool
