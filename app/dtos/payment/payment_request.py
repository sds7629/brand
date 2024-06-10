from typing import Sequence

from pydantic import dataclasses

@dataclasses.dataclass
class PaymentRequest:
    user_id: str
    order_id: str
    price: int
    cart_id: Sequence[str]