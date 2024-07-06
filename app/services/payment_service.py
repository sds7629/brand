from datetime import datetime
from typing import Sequence

from bson import ObjectId

from app.dtos.payment.payment_request import PaymentRequest
from app.entities.collections import CartCollection, OrderCollection
from app.entities.collections.payment.payment_collection import PaymentCollection
from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NoSuchContentException


async def find_payment(user: ShowUserDocument, payment_request: PaymentRequest) -> tuple[PaymentDocument, int]:

    if order := await OrderCollection.find_by_id(ObjectId(payment_request.order_id)):
        raise NoSuchContentException(response_message="주문 정보를 찾을 수 없습니다.")

    if order.user == user:
        updated_data = await OrderCollection.update_by_order_id(
            ObjectId(payment_request.order_id), {"is_payment": True}
        )
        payment_result = await PaymentCollection.insert_one(
            user=user,
            order=order.id,
            items=[(await CartCollection.find_by_id(ObjectId(cart_id))).item for cart_id in payment_request.cart_id],
            payment_time=datetime.utcnow(),
            total_price=payment_request.total_price,
        )

        [await CartCollection.delete_by_id(ObjectId(cart_id)) for cart_id in payment_request.cart_id]
        return (payment_result, updated_data)
    raise NoPermissionException(response_message="결제 유저와 요청 유저가 다릅니다.")


async def get_history(user: ShowUserDocument) -> Sequence[PaymentDocument]:
    if (user_history := await PaymentCollection.find_by_user_id(user.id)) is None:
        raise NoSuchContentException(response_message="주문 내역이 없습니다.")
    return user_history
