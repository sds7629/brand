import dataclasses

from app.entities.collections.users.user_document import DeliveryDocument


@dataclasses.dataclass
class DeliveryResponse:
    id: str
    name: str
    email: str
    post_code: str
    address: str
    detail_address: str
    recipient_phone: str
    requirements: str
    is_base_delivery: bool


@dataclasses.dataclass
class UserProfileResponse:
    id: str
    name: str
    nickname: str
    email: str
    delivery_area: list[DeliveryResponse] | None
