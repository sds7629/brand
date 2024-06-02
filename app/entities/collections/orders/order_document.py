from datetime import datetime
from typing import Sequence

from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_document import (
    ShowUserDocument,
)

from app.config import Config


@dataclasses.dataclass(config=Config)
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    payment_item: Sequence[PaymentDocument]
    merchant_id: str
    post_code: str
    address: str
    detail_address: str
    post_text: str | None
    orderer_name: str
    phone_num: str
    payment_method: str
    ordering_date: datetime
    is_payment: bool
