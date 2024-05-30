import dataclasses

from app.entities.collections.users.user_document import DeliveryDocument


@dataclasses.dataclass
class UserProfileResponse:
    id: str
    name: str
    nickname: str
    email: str
    gender: str
    delivery_area: list[DeliveryDocument] | None
