from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class PaymentRequest:
    order_id: str
    total_price: int
    cart_id: Sequence[str]
