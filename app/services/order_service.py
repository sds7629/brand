import asyncio
import uuid

from bson import ObjectId

from app.dtos.order.order_creation_request import OrderCreationRequest, PreOrderRequest
from app.entities.collections import CartCollection, ItemCollection, UserCollection
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.orders.order_document import (
    OrderDocument,
    OrderItem,
    PreOrderDocument,
)
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NotFoundException, ValidationException
from app.utils.payment_util import PaymentUtil


async def get_user_orders(user: ShowUserDocument) -> list[OrderDocument] | None:
    order = await OrderCollection.find_by_user_id(ObjectId(user.id))
    if order is None:
        raise NotFoundException(response_message="주문한 이력이 없습니다.")
    return order


async def pre_order_cart(
    user: ShowUserDocument, pre_order_creation_request: PreOrderRequest
) -> PreOrderDocument | None:
    user_document = await UserCollection.find_by_id(ObjectId(user.id))
    user_base_delivery = [delivery for delivery in user_document.delivery_area if delivery.is_base_delivery]
    merchant_id = await PaymentUtil.generate_merchant_id()

    match pre_order_creation_request.type:
        case "cart":
            order_item_from_cart = [
                await CartCollection.find_by_id(ObjectId(cart_id)) for cart_id in pre_order_creation_request.cart_id
            ]
            compare_cart_from_user = [cart.user.id == user.id for cart in order_item_from_cart]

            if all(compare_cart_from_user) is False:
                raise NoPermissionException(response_message="권한이 없습니다.")

            ordering_item = [
                {
                    "order_item_id": cart.item.id,
                    "order_item_name": cart.item.name,
                    "order_item_images": cart.item.image_urls,
                    "order_item_price": cart.item.price,
                    "order_item_quantity": cart.quantity,
                    "selected_options": cart.options,
                }
                for cart in order_item_from_cart
            ]
            total_price = sum([cart.total_price for cart in order_item_from_cart])

        case "item":
            order_item = await ItemCollection.find_by_id(ObjectId(pre_order_creation_request.options[0].item_id))
            ordering_item = [
                {
                    "order_item_id": order_item.id,
                    "order_item_name": order_item.name,
                    "order_item_images": order_item.image_urls,
                    "order_item_price": order_item.price,
                    "order_item_quantity": item.quantity,
                    "selected_options": item.option,
                }
                for item in pre_order_creation_request.options
            ]
            total_price = sum([order_item.price * item.quantity for item in pre_order_creation_request.options])

        case _:
            raise ValidationException(response_message="타입이 올바르지 않습니다.")

    if user_base_delivery:
        return PreOrderDocument(
            user=user,
            merchant_id=merchant_id,
            email=user_base_delivery[0].email,
            post_code=user_base_delivery[0].post_code,
            address=user_base_delivery[0].address,
            detail_address=user_base_delivery[0].detail_address,
            recipient_name=user.name,
            phone_num=user_base_delivery[0].recipient_phone,
            requirements=user_base_delivery[0].requirements,
            total_price=total_price,
            ordering_item=ordering_item,
        )
    else:
        return PreOrderDocument(
            user=user,
            merchant_id=merchant_id,
            email=None,
            post_code=None,
            address=None,
            detail_address=None,
            recipient_name=user.name,
            phone_num=None,
            requirements=None,
            total_price=total_price,
            ordering_item=ordering_item,
        )


async def create_order(user: ShowUserDocument, order_creation_request: OrderCreationRequest) -> OrderDocument:
    co_item_list = [
        ItemCollection.find_by_id(ObjectId(item_info.item_id)) for item_info in order_creation_request.item_info
    ]
    item_list = await asyncio.gather(*co_item_list)

    option_exist = [
        True
        for item, item_info in zip(item_list, order_creation_request.item_info)
        if item_info.option not in item.options.keys()
    ]
    if bool(option_exist):
        raise ValidationException(response_message="잘못된 옵션입니다.")

    quantity_exist = [
        True
        for item, item_info in zip(item_list, order_creation_request.item_info)
        if item.options[item_info.option] >= item_info.quantity
    ]

    if not bool(quantity_exist):
        raise ValidationException(response_message="재고 수량보다 요청 수량이 많습니다.")

    order_item_list = [
        OrderItem(
            item=item,
            option=item_info.option,
            quantity=item_info.quantity,
        )
        for item, item_info in zip(item_list, order_creation_request.item_info)
    ]

    total_price = sum(
        [item.price * item_info.quantity for item, item_info in zip(item_list, order_creation_request.item_info)]
    )

    if order_creation_request.total_price == total_price:
        return await OrderCollection.insert_one(
            user=user,
            order_item=order_item_list,
            merchant_id=order_creation_request.merchant_id,
            recipient_name=order_creation_request.recipient_name,
            post_code=order_creation_request.post_code,
            address=order_creation_request.address,
            detail_address=order_creation_request.detail_address,
            requirements=order_creation_request.requirements,
            phone_num=order_creation_request.phone_num,
            total_price=order_creation_request.total_price,
        )
    else:
        raise ValidationException(response_message="요청 금액과 결제 금액이 같지 않습니다.")
