import asyncio

from app.dtos.order.order_creation_request import OrderCreationRequest
from app.dtos.order.order_request import OrderRequest
from app.entities.collections import ItemCollection, CartCollection

from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import OrderNotFoundException

from bson import ObjectId


async def get_user_orders(order_request: OrderRequest) -> list[OrderDocument] | None:
    order = await OrderCollection.find_by_user_id(ObjectId(order_request.user_id))
    if order is None:
        raise OrderNotFoundException(response_message="주문한 이력이 없습니다.")
    return order


async def create_order(user: ShowUserDocument, order_creation_request: OrderCreationRequest) -> None:
    user_cart_item = CartCollection.find_user_cart(ObjectId(user.id))

