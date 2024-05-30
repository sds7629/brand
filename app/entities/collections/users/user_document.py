from datetime import datetime
from typing import Optional

from pydantic import dataclasses, field_validator
from pydantic.dataclasses import Field

from app.config import Config
from app.entities.collections.base_document import BaseDocument


@dataclasses.dataclass(config=Config)
class DeliveryDocument:
    user_id: str
    recipient: str
    code: str
    address: str
    detail_address: str
    recipient_phone: str
    requirements: str
    updated_at: Optional[datetime] = None
    is_base_delivery: bool = False


@dataclasses.dataclass
class UserDocument(BaseDocument):
    user_id: str
    email: str
    name: str
    hash_pw: str
    gender: str
    nickname: str
    phone_num: str
    login_method: str
    is_authenticated: bool
    is_delete: bool
    delivery_area: list[DeliveryDocument] = Field(default_factory=list, alias="delivery_area")


@dataclasses.dataclass(config=Config)
class ShowUserDocument(BaseDocument):
    user_id: str
    email: str
    name: str
    gender: str
    nickname: str
    is_delete: bool
    delivery_area: list[DeliveryDocument] = Field(default_factory=list, alias="delivery_area")
