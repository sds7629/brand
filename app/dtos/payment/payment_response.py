from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class PaymentResponse:
    user_name: str
    item_name: Sequence[str]
    total_price: int
