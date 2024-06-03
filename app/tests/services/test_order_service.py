from app.dtos.order.order_creation_request import OrderRequest
from app.services.order_service import find_order_user_nickname


async def test_유저주문_찾기() -> None:
    order_request = OrderRequest(user_nickname="admin")
    result = await find_order_user_nickname(order_request)

    assert len(result) == 1
