import asyncio
from dataclasses import asdict
from typing import Sequence

from bson import ObjectId

from app.dtos.cart.cart_creation_request import OneCartCreationRequest
from app.dtos.cart.cart_update_request import CartUpdateRequest
from app.entities.collections import ItemCollection, UserCollection
from app.entities.collections.carts.cart_collection import CartCollection
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    NoPermissionException,
    NoSuchContentException,
    ValidationException,
)


async def get_user_carts(user_data: ShowUserDocument) -> Sequence[CartDocument]:
    user_carts = await CartCollection.find_user_cart(ObjectId(user_data.id))

    return user_carts


async def create_cart(
    user_data: ShowUserDocument, cart_creation_request: OneCartCreationRequest
) -> tuple[CartDocument, ...]:
    user = await UserCollection.find_by_id(user_data.id)
    item = await ItemCollection.find_by_id(ObjectId(cart_creation_request.item_id))
    insert_cart_data = [
        CartCollection.insert_one(
            user=user,
            item=item,
            quantity=option.quantity,
            options=option.color_size,
            total_price=item.price * option.quantity,
        )
        for option in cart_creation_request.options
        if item.options[option.color_size] >= option.quantity
    ]
    result = await asyncio.gather(*insert_cart_data)
    if result:
        return result
    else:
        raise ValidationException(response_message="요청이 잘못 되었습니다.")


async def update_cart(user: ShowUserDocument, cart_id: str, cart_update_request: CartUpdateRequest) -> int:
    cart = await CartCollection.find_by_id(ObjectId(cart_id))
    if cart.user != user:
        raise NoPermissionException(response_message="접근 권한이 없습니다.")

    if (cart_update_request.options is not None) and (cart_update_request.options not in cart.item.options.keys()):
        raise ValidationException(response_message="잘못된 요청입니다.")

    if (cart_update_request.quantity is not None) and (
        cart_update_request.quantity
        > cart.item.options[
            f"{cart_update_request.options if cart_update_request.options is not None else cart.item.options[f'{cart.options}']}"
        ]
    ):
        raise ValidationException(response_message="잘못된 요청입니다.")

    if len(data := {key: val for key, val in asdict(cart_update_request).items() if val is not None}):
        updated_itme_count = await CartCollection.update_by_id(ObjectId(cart_id), data)
        return updated_itme_count
    raise NoSuchContentException(response_message="No Content")


async def delete_cart(user: ShowUserDocument, cart_id: ObjectId) -> None:
    cart = await CartCollection.find_by_id(cart_id)
    if cart.user != user:
        raise NoPermissionException(response_message="접근 권한이 없습니다.")
    await CartCollection.delete_by_id(cart.id)
