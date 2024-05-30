from typing import Sequence

from pydantic import dataclasses

@dataclasses.dataclass
class CartCreationRequest:
    item_id : Sequence[str]
    mount: int