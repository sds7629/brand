from pydantic import dataclasses


@dataclasses.dataclass
class DeliveryRequest:
    name: str
    email: str
    post_code: str
    address: str
    detail_address: str
    recipient_phone: str
    requirements: str
    is_base_delivery: bool


@dataclasses.dataclass
class UpdateDeliveryRequest:
    name: str | None = None
    email: str | None = None
    post_code: str | None = None
    address: str | None = None
    detail_address: str | None = None
    recipient_phone: str | None = None
    requirements: str | None = None
    is_base_delivery: bool | None = None
