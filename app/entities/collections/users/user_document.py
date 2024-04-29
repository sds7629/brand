import dataclasses
import datetime
from dataclasses import field

from app.entities.collections.base_document import BaseDocument


@dataclasses.dataclass
class DeliveryDocument:
    _id_user: str
    recipient: str
    code: str
    address: str
    detail_address: str
    recipient_phone: str
    requirements: str
    updated_at: datetime.time() = None
    is_base_delivery: bool = False


@dataclasses.dataclass
class UserDocument(BaseDocument):
    user_id: str
    email: str
    name: str
    hash_pw: str
    gender: str
    nickname: str
    login_method: str
    is_authenticated: bool
    is_delete: bool
    delivery_area: list[DeliveryDocument] | None = field(default_factory=list)
