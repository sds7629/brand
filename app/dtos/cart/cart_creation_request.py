from typing import Sequence

from pydantic import dataclasses


@dataclasses.dataclass
class CartOption:
    quantity: int
    color_size: str


@dataclasses.dataclass
class OneCartCreationRequest:
    item_id: str
    options: Sequence[CartOption]


@dataclasses.dataclass
class CartCreationRequest:
    items: Sequence[OneCartCreationRequest]
