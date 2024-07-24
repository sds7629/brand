from pydantic import Field, dataclasses


@dataclasses.dataclass
class PaymentRequest:
    amount: int
    payment_key: str
    payment_type: str
    order_id: str


@dataclasses.dataclass
class FailPaymentRequest:
    code: str
    message: str
    order_id: str


@dataclasses.dataclass
class SetPaymentRequest:
    payment_method: str
    payment_name: str
    merchant_id: str
    amount: int
