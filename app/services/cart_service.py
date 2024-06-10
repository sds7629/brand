import asyncio
from typing import Sequence

from bson import ObjectId

from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.entities.collections import ItemCollection, UserCollection
from app.entities.collections.carts.cart_collection import CartCollection
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import ValidationException


async def get_user_carts(user_data: ShowUserDocument) -> Sequence[CartDocument]:
    user_carts = await CartCollection.find_user_cart(ObjectId(user_data.id))

    return user_carts


async def create_cart(
    user_data: ShowUserDocument, cart_creation_request: CartCreationRequest
) -> tuple[CartDocument, ...]:
    user = await UserCollection.find_by_id(user_data.id)
    item_list = [ItemCollection.find_by_id(ObjectId(item.item_id)) for item in cart_creation_request.items]
    insert_cart_data = [
        CartCollection.insert_one(
            user=user,
            item=item_dto,
            quantity=item.quantity,
            color=item.color,
            total_price=item.quantity * item_dto.price,
        )
        for item_dto, item in zip(await asyncio.gather(*item_list), cart_creation_request.items)
        if item.quantity <= item_dto.quantity
    ]
    result = await asyncio.gather(*insert_cart_data)
    if result:
        return result
    else:
        raise ValidationException(response_message="요청이 잘못 되었습니다.")
