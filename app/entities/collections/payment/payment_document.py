from datetime import datetime

from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.enums.payment_codes import PaymentMethodCode


@dataclasses.dataclass
class PaymentDocument(BaseDocument):
    user: ShowUserDocument
    payment_name: str
    merchant_id: str
    total_price: int
    payment_time: datetime
    payment_method: PaymentMethodCode | None
    payment_status: bool
    fail_reason: str | None
