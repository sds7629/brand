import asyncio

from app.dtos.order.order_creation_request import OrderCreationRequest
from app.dtos.order.order_request import OrderRequest
from app.entities.collections import CartCollection, UserCollection

from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import OrderNotFoundException, NoSuchElementException



from bson import ObjectId


async def get_user_orders(order_request: OrderRequest) -> list[OrderDocument] | None:
    order = await OrderCollection.find_by_user_id(ObjectId(order_request.user_id))
    if order is None:
        raise OrderNotFoundException(response_message="주문한 이력이 없습니다.")
    return order


async def create_order(user: ShowUserDocument, order_creation_request: OrderCreationRequest) -> OrderDocument | None:
    user_cart_item = await CartCollection.find_user_cart(ObjectId(user.id))
    if user_cart_item is None:
        raise NoSuchElementException(response_message="장바구니가 비어있습니다.")
    order_item = [await CartCollection.find_by_id(ObjectId(cart_id)) for cart_id in order_creation_request.cart_id]
    compare_bool = [cart.user.id == user.id for cart in order_item]

    if all(compare_bool) is False:
        return None

    user_document = await UserCollection.find_by_id(ObjectId(user.id))
    user_base_delivery = [delivery for delivery in user_document.delivery_area if delivery.is_base_delivery == True]
    if user_base_delivery:
        order = await OrderCollection.insert_one(
            user = user,
            post_code = user_base_delivery[0].post_code,
            address = user_base_delivery[0].address,
            detail_address = user_base_delivery[0].detail_address,
            phone_num = user_base_delivery[0].recipient_phone,
            orderer_name = user_base_delivery[0].name,
            requirements = user_base_delivery[0].requirements,
        )
    else:
        order = await OrderCollection.insert_one(
            user = user,

        )

    return order
