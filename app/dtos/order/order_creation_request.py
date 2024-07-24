from typing import Annotated, Literal, Sequence, Union

from fastapi import Body
from pydantic import dataclasses
from pydantic.dataclasses import Field

from app.config import Config
from app.utils.enums.payment_codes import PaymentMethodCode


@dataclasses.dataclass
class OrderItemCreationRequest:
    item_id: str
    option: str
    quantity: int


@dataclasses.dataclass(config=Config)
class PreOrderCartCreationRequest:
    type: Literal["cart"] = "cart"
    cart_id: Sequence[str] = Field(default_factory=list)


@dataclasses.dataclass(config=Config)
class PreOrderItemCreationRequest:
    type: Literal["item"] = "item"
    options: Sequence[OrderItemCreationRequest] = Field(default_factory=list)


PreOrderRequest = Annotated[Union[PreOrderCartCreationRequest, PreOrderItemCreationRequest], Body(discriminator="type")]


@dataclasses.dataclass(config=Config)
class OrderCreationRequest:
    item_info: Sequence[OrderItemCreationRequest]
    merchant_id: str
    recipient_name: str
    post_code: str
    address: str
    detail_address: str
    phone_num: str
    order_name: str
    requirements: str | None
    payment_method: PaymentMethodCode
    total_price: int
