from typing import Sequence

from pydantic import dataclasses
from app.entities.collections.base_document import BaseDocument


@dataclasses.dataclass
class DisCountCouponComponent:
    type: str
    discount_price: int


@dataclasses.dataclass
class RatioCouponComponent:
    type: str
    discount_ratio: int


@dataclasses.dataclass
class CouponDocument(BaseDocument):
    name: str
    components: Sequence[CouponComponent]