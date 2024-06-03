from typing import Sequence

from pydantic import dataclasses

from app.config import Config


@dataclasses.dataclass(config=Config)
class OrderCreationRequest:
    cart_id: Sequence[str]
