from app.dtos.order.order_request import OrderRequest
from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.orders.order_collection import OrderCollection
from app.exceptions import OrderNotFoundException


async def find_order_user_nickname(order_request: OrderRequest) -> list[OrderDocument] | None:
    order = await OrderCollection.find_by_user_nickname(order_request.user_nickname)
    if order is None:
        raise OrderNotFoundException(response_message="주문한 이력이 없습니다.")
    return order