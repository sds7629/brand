from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class OneCartCreationRequest:
    item_id: str
    quantity: int
    color: str


@dataclasses.dataclass
class CartCreationRequest:
    items: Sequence[OneCartCreationRequest]
