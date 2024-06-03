from datetime import datetime

from bson import ObjectId

from app.entities.collections import ItemCollection
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_collection import UserCollection
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode
from app.utils.payment_util import PaymentUtil


async def test_order_insert_one() -> None:
    user = await UserCollection.find_by_nickname("admin")
    post_text = "문 앞에 놔주세요"
    item = await ItemCollection.find_by_id(ObjectId("665b07704f4f6490716bced6"))
    payment_item = PaymentDocument(
        user=user,
        item=item,
        item_option="white-1",
        total_price=item.price * 3,
        payment_time=datetime.utcnow(),
        is_reviewed=False,
    )
    post_code = "0110"
    address = "서울시 종로구"
    detail_address = "지층동"
    payment_method = "Naver Pay"
    phone_num = "010-2222-1111"

    result = await OrderCollection.insert_one(
        user=user,
        payment_items=[payment_item],
        merchant_id=await PaymentUtil.create_uuid_to_sting(),
        post_code=post_code,
        address=address,
        detail_address=detail_address,
        orderer_name=user.name,
        phone_num=phone_num,
        payment_method=payment_method,
        post_text=post_text,
    )

    assert result.user == user
    assert result.is_payment == False
    assert result.payment_item[0].is_reviewed == False
