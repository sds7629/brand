from bson import ObjectId

from app.dtos.order.order_creation_request import (
    OrderCreationRequest,
    PreOrderCreationRequest,
)
from app.entities.collections import CartCollection, UserCollection
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.orders.order_document import (
    OrderDocument,
    PreOrderDocument,
)
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    ItemQuantityException,
    NoPermissionException,
    NoSuchElementException,
    OrderNotFoundException,
    ValidationException,
)
from app.utils.payment_util import PaymentUtil


async def get_user_orders(user: ShowUserDocument) -> list[OrderDocument] | None:
    order = await OrderCollection.find_by_user_id(ObjectId(user.id))
    if order is None:
        raise OrderNotFoundException(response_message="주문한 이력이 없습니다.")
    return order


async def pre_order(
    user: ShowUserDocument, pre_order_creation_request: PreOrderCreationRequest
) -> PreOrderDocument | None:
    user_cart_item = await CartCollection.find_user_cart(ObjectId(user.id))
    if user_cart_item is None:
        raise NoSuchElementException(response_message="장바구니가 비어있습니다.")
    order_item = [await CartCollection.find_by_id(ObjectId(cart_id)) for cart_id in pre_order_creation_request.cart_id]
    compare_cart_from_user = [cart.user.id == user.id for cart in order_item]

    if all(compare_cart_from_user) is False:
        raise NoPermissionException(response_message="권한이 없습니다.")

    user_document = await UserCollection.find_by_id(ObjectId(user.id))
    user_base_delivery = [delivery for delivery in user_document.delivery_area if delivery.is_base_delivery == True]
    if user_base_delivery:
        order = PreOrderDocument(
            user=user,
            merchant_id=None,
            email=user_base_delivery[0].email,
            post_code=user_base_delivery[0].post_code,
            address=user_base_delivery[0].address,
            detail_address=user_base_delivery[0].detail_address,
            order_name=user.name,
            phone_num=user_base_delivery[0].recipient_phone,
            requirements=user_base_delivery[0].requirements,
            payment_method=None,
            is_payment=False,
            total_price=sum([one_cart.total_price for one_cart in order_item]),
        )
    else:
        order = PreOrderDocument(
            user=user,
            merchant_id=None,
            email=None,
            post_code=None,
            address=None,
            detail_address=None,
            order_name=user.name,
            phone_num=None,
            requirements=None,
            payment_method=None,
            is_payment=False,
            total_price=sum([one_cart.total_price for one_cart in order_item]),
        )

    return order


async def create_order(user: ShowUserDocument, order_creation_request: OrderCreationRequest) -> OrderDocument:
    merchant_id = await PaymentUtil.generate_merchant_id()
    carts = [await CartCollection.find_by_id(ObjectId(cart_id)) for cart_id in order_creation_request.cart_id]
    quantity_confirm = [cart for cart in carts if cart.quantity > cart.item.item_quantity]
    if quantity_confirm:
        raise ItemQuantityException(response_message="주문하시는 수량이 남아있는 상품 갯수 보다 많습니다.")

    cart_price_data = sum([cart.total_price for cart in carts])
    if cart_price_data == order_creation_request.total_price:
        return await OrderCollection.insert_one(
            user=user,
            merchant_id=merchant_id,
            email=order_creation_request.email,
            post_code=order_creation_request.post_code,
            address=order_creation_request.address,
            detail_address=order_creation_request.detail_address,
            order_name=order_creation_request.order_name,
            phone_num=order_creation_request.phone_num,
            payment_method=order_creation_request.payment_method,
            requirements=order_creation_request.requirements,
            total_price=order_creation_request.total_price,
            ordering_item=[cart.item.id for cart in carts],
        )
    else:
        raise ValidationException(response_message="잘못된 요청입니다.")
