from datetime import datetime
from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class BasePaymentResponse:
    order_id: str
    amount: int
    payment_key: str


@dataclasses.dataclass
class PaymentHistoryResponse:
    merchant_id: str
    payment_name: str
    total_price: int
    payment_time: datetime
    payment_method: str
    payment_status: str


@dataclasses.dataclass
class FailPaymentResponse:
    code: str
    message: str
    merchant_id: str


@dataclasses.dataclass
class CancelPaymentResponse:
    message: str
