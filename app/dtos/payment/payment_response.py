from datetime import datetime
from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class PaymentResponse:
    user_name: str
    item_name: Sequence[str]
    total_price: int


@dataclasses.dataclass
class PaymentHistoryResponse:
    order: str
    item_name: Sequence[str]
    total_price: int
    payment_time: datetime
