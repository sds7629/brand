from bson import ObjectId
from app.entities.collections import ItemCollection
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import DeliveryDocument


async def test_order_insert_one() -> None:
    user = await UserCollection.find_by_nickname("admin")
    ordering_request = "문 앞에 놔주세요"
    ordering_item = await ItemCollection.find_by_id(ObjectId("664ed8aab42caf93de9464b6"))
    ordering_item_mount = 3
    zip_code = "0110"
    address = user.delivery_area[0]
    detail_address = "지층동"
    payment_method = "Naver Pay"
    total_price = ordering_item.price * ordering_item_mount

    result = await OrderCollection.insert_one(
        user = user,
        ordering_request=ordering_request,
        ordering_item=ordering_item,
        ordering_item_mount = ordering_item_mount,
        zip_code = zip_code,
        address = address,
        detail_address = detail_address,
        payment_method = payment_method,
        total_price = total_price,

    )

    assert result.user == user
    assert result.total_price == ordering_item.price * ordering_item_mount