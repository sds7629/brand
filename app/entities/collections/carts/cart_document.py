from typing import Sequence

from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument

from app.config import Config


@dataclasses.dataclass(config = Config)
class CartDocument(BaseDocument):
    user: ShowUserDocument
    items: Sequence[ItemDocument]
    mount: int
    total_price: int