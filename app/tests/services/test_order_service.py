from bson import ObjectId

from app.dtos.order.order_request import OrderRequest
from app.services.order_service import get_user_orders


async def test_get_user_orders() -> None:
    user_id = "665ddfbe4c1114a333c3e49c"

    order_request = OrderRequest(user_id=user_id)
    orders = await get_user_orders(order_request)

    assert len(orders)
