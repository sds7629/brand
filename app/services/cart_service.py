import asyncio

from typing import Sequence

from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.entities.collections import ItemCollection
from app.entities.collections.carts.cart_collection import CartCollection
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument

from bson import ObjectId

from app.exceptions import ValidationException


async def get_user_carts(user_data: ShowUserDocument) -> Sequence[CartDocument]:
    user_carts = await CartCollection.find_user_cart(ObjectId(user_data.id))

    return user_carts


async def create_cart(user_data: ShowUserDocument, cart_creation_request: CartCreationRequest) -> CartDocument:
    co_item_list = [ItemCollection.find_by_id(ObjectId(item)) for item in cart_creation_request.item_id]
    item_list = await asyncio.gather(*co_item_list)
    total_price = sum([item.price for item in item_list])
    create_user_cart = await CartCollection.insert_one(
        user = user_data,
        items = item_list,
        mount = cart_creation_request.mount,
        total_price = total_price
    )
    if create_user_cart:
        return create_user_cart
    else:
        raise ValidationException(response_message="요청이 잘못 되었습니다.")