from datetime import datetime
from typing import Optional

from pydantic import dataclasses
from pydantic.dataclasses import Field

from app.config import Config
from app.entities.collections.base_document import BaseDocument


@dataclasses.dataclass(config=Config)
class DeliveryDocument:
    name: str
    email: str
    post_code: str
    address: str
    detail_address: str
    recipient_phone: str
    requirements: str
    updated_at: Optional[datetime] = None
    is_base_delivery: bool = False


@dataclasses.dataclass
class UserDocument(BaseDocument):
    user_id: str | None
    email: str
    name: str | None
    hash_pw: str | None
    nickname: str | None
    phone_num: str | None
    point: int
    login_method: str
    sns_confirm: bool
    is_authenticated: bool
    is_policy: bool
    is_admin: bool
    is_delete: bool
    delivery_area: list[DeliveryDocument] = Field(default_factory=list, alias="delivery_area")


@dataclasses.dataclass
class SocialUserDocument(BaseDocument):
    email: str
    name: str
    nickname: str | None
    login_method: str
    sns_confirm: bool
    is_policy: bool
    delivery_area: list[DeliveryDocument] = Field(default_factory=list, alias="delivery_area")


@dataclasses.dataclass(config=Config)
class ShowUserDocument(BaseDocument):
    user_id: str
    email: str
    name: str
    nickname: str
    login_method: str
    point: int
    is_delete: bool
    is_admin: bool
    delivery_area: list[DeliveryDocument] = Field(default_factory=list, alias="delivery_area")
