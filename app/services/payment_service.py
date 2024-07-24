import asyncio
import base64
from datetime import datetime
from typing import Sequence

import aiohttp
from bson import ObjectId

from app.config import TOSS_SECRET_KEY
from app.dtos.payment.payment_request import (
    FailPaymentRequest,
    PaymentRequest,
    SetPaymentRequest,
)
from app.entities.collections import CartCollection, ItemCollection, OrderCollection
from app.entities.collections.payment.payment_collection import PaymentCollection
from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    NoPermissionException,
    NoSuchContentException,
    ValidationException,
)
from app.utils.enums.payment_codes import PaymentMethodCode

toss_secret = TOSS_SECRET_KEY + ":"
toss_key = base64.b64encode(toss_secret.encode("utf-8"))
toss_key_str = toss_key.decode("utf-8")


async def get_history(user: ShowUserDocument) -> Sequence[PaymentDocument]:
    user_history = await PaymentCollection.find_by_user_id(user.id)
    return user_history


async def set_payment(user: ShowUserDocument, payment_request: SetPaymentRequest) -> PaymentDocument:
    order = await OrderCollection.find_by_merchant_id(payment_request.merchant_id)
    if order.user != user:
        raise NoPermissionException(response_message="권한이 없습니다.")
    payment = await PaymentCollection.insert_one(
        user=user,
        merchant_id=payment_request.merchant_id,
        payment_name=payment_request.payment_name,
        total_price=payment_request.amount,
        payment_method=PaymentMethodCode(payment_request.payment_method),
        payment_time=datetime.utcnow(),
    )

    return payment


async def success_payment(payment_request: PaymentRequest) -> None:
    payment = await PaymentCollection.find_by_merchant_id(payment_request.order_id)
    order = await OrderCollection.find_by_merchant_id(payment_request.order_id)
    if payment is None:
        raise NoSuchContentException(response_message="잘못된 요청입니다.")

    if order is None:
        raise NoSuchContentException(response_message="해당 주문이 없습니다.")

    if not ((payment.total_price == payment_request.amount) and (payment.total_price == order.total_price)):
        raise ValidationException(response_message="금액이 일치하지 않습니다.")

    confirm_url = "https://api.tosspayments.com/v1/payments/confirm"
    cancel_url = f"https://api.tosspayments.com/v1/payments/{payment_request.payment_key}/cancel"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {toss_key_str}",
        "Cross-Origin-Opener-Policy": "same-origin-allow-popups",
    }

    data = {
        "paymentKey": payment_request.payment_key,
        "orderId": payment_request.order_id,
        "amount": payment_request.amount,
    }

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        headers=headers,
    ) as client:
        async with client.post(confirm_url, json=data) as response:
            if response.status == 200:
                payment_data = await response.json()
            else:
                raise ValidationException(response_message="에러가 발생했습니다.")

        real_pay = payment_data["balanceAmount"]

        if real_pay != payment_request.amount:
            async with client.post(
                cancel_url,
                json={
                    "paymentKey": payment_request.payment_key,
                    "cancelReason": "요청 금액 오류",
                },
            ) as response:
                if response.status == 200:
                    raise ValidationException("실 결제 금액이 요청 금액과 다릅니다.")

        await OrderCollection.update_by_merchant_id(
            merchant_id=payment_request.order_id,
            data={
                "is_payment": True,
            },
        )

        await PaymentCollection.update_by_id(
            payment_id=payment.id,
            data={
                "payment_status": True,
            },
        )

        order_item_list = [
            ItemCollection.update_quantity_by_id(
                object_id=ObjectId(_item.item.id),
                option=_item.option,
                quantity=_item.quantity,
            )
            for _item in order.order_item
        ]

        await asyncio.gather(*order_item_list)

        cart_list = [
            CartCollection.delete_by_item(
                item_id=ObjectId(_item.item.id),
                user_id=payment.user.id,
                option=_item.option,
            )
            for _item in order.order_item
        ]

        await asyncio.gather(*cart_list)

    return


async def fail_payment(payment_request: FailPaymentRequest) -> None:
    payment = await PaymentCollection.update_by_merchant_id(
        merchant_id=payment_request.order_id, data={"fail_reason": payment_request.code + payment_request.message}
    )
    if payment == 0:
        raise NoSuchContentException(response_message="결제 내역을 찾을 수 없습니다.")
    return
