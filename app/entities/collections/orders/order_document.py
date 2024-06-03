from datetime import datetime

from pydantic import dataclasses

from app.config import Config
from app.entities.collections.base_document import BaseDocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass(config=Config)
class OrderDocument(BaseDocument):
    user: ShowUserDocument
    merchant_id: str | None
    post_code: str | None
    address: str | None
    detail_address: str | None
    requirements: str | None
    orderer_name: str | None
    phone_num: str | None
    payment_method: str | None
    ordering_date: datetime
    is_payment: bool
