import asyncio
from typing import Sequence

from bson import ObjectId

from app.dtos.cart.cart_creation_request import OneCartCreationRequest
from app.entities.collections import ItemCollection, UserCollection
from app.entities.collections.carts.cart_collection import CartCollection
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NotPermissionException, ValidationException


async def get_user_carts(user_data: ShowUserDocument) -> Sequence[CartDocument]:
    user_carts = await CartCollection.find_user_cart(ObjectId(user_data.id))

    return user_carts


async def create_cart(
    user_data: ShowUserDocument, cart_creation_request: OneCartCreationRequest
) -> tuple[CartDocument, ...]:
    user = await UserCollection.find_by_id(user_data.id)
    item = await ItemCollection.find_by_id(ObjectId(cart_creation_request.item_id))
    # insert_cart_data = [
    #     CartCollection.insert_one(
    #         user=user,
    #         item=item_dto,
    #         quantity=item.quantity,
    #         options=item.color,
    #         total_price=item.quantity * item_dto.price,
    #     )
    #     for item_dto, item in zip(await asyncio.gather(*item_list), cart_creation_request.items)
    #     if item.quantity <= item_dto.quantity
    # ]
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


async def delete_cart(user: ShowUserDocument, cart_id: ObjectId) -> None:
    cart = await CartCollection.find_by_id(cart_id)
    if cart.user != user:
        raise NotPermissionException(response_message="접근 권한이 없습니다.")
    await CartCollection.delete_by_id(cart.id)
