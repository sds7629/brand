from typing import Annotated, Union

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.order.order_creation_request import OrderCreationRequest, PreOrderRequest
from app.dtos.order.order_response import (
    BaseOrderResponse,
    CreateOrderResponse,
    OrderItemResponse,
    OrderResponse,
    PreOrderResponse,
)
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NotFoundException, ValidationException
from app.services.order_service import create_order, get_user_orders, pre_order_cart
from app.utils.utility import TimeUtil

router = APIRouter(prefix="/v1/orders", tags=["orders"], redirect_slashes=False)


@router.get(
    "",
    description="유저 주문 정보 가져오기",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_orders(user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> OrderResponse:
    orders = await get_user_orders(user)

    return OrderResponse(
        order_list=[
            BaseOrderResponse(
                id=str(order.id),
                merchant_id=order.merchant_id,
                address=order.address,
                detail_address=order.detail_address,
                recipient_name=order.recipient_name,
                requirements=order.requirements,
                ordering_date=await TimeUtil.get_created_at_from_id(str(order.id)),
                items=[
                    OrderItemResponse(
                        item_name=item.item.name,
                        item_option=item.option,
                        item_price=item.item.price,
                        image_urls=item.item.image_urls,
                    )
                    for item in order.order_item
                ],
            )
            for order in orders
        ]
    )


@router.post(
    "/start",
    description="결제 주문",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_pre_order(
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    pre_order_creation_request: PreOrderRequest,
) -> PreOrderResponse:
    try:
        order = await pre_order_cart(user, pre_order_creation_request)
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message},
        )
    return PreOrderResponse(
        user_id=order.user.user_id,
        merchant_id=order.merchant_id,
        email=order.user.email,
        post_code=order.post_code,
        address=order.address,
        detail_address=order.detail_address,
        phone_num=order.phone_num,
        recipient_name=order.recipient_name,
        requirements=order.requirements,
        total_price=order.total_price,
        ordering_item=[
            OrderItemResponse(
                item_id=item_info["order_item_id"],
                option=item_info["selected_options"],
                quantity=item_info["order_item_quantity"],
            )
            for item_info in order.ordering_item
        ],
    )


@router.post(
    "/done",
    description="결제 주문 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_order(
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    order_creation_request: OrderCreationRequest
) -> CreateOrderResponse:
    try:
        order = await create_order(user, order_creation_request)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )

    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )

    return CreateOrderResponse(order_id=str(order.id))
