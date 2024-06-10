from typing import Annotated

import aiohttp
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.order.order_creation_request import (
    OrderCreationRequest,
    PreOrderCreationRequest,
)
from app.dtos.order.order_response import (
    BaseOrderResponse,
    CreateOrderResponse,
    OrderResponse,
    PreOrderResponse, OrderItemResponse,
)
from app.dtos.payment.payment_request import PaymentRequest
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    ItemQuantityException,
    NoPermissionException,
    NoSuchElementException,
    ValidationException,
)
from app.services.order_service import create_order, get_user_orders, pre_order, find_payment
from app.config import PORT_ONE_SECRET_KEY, STORE_ID



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
                merchant_id = order.merchant_id,
                address=order.address,
                detail_address=order.detail_address,
                order_name=order.order_name,
                requirements=order.requirements,
                ordering_date=order.ordering_date,
                item=[OrderItemResponse(
                    name = item.name,
                    price = item.price,
                    size = item.size,
                    color = item.color,
                    image_url = item.image_url,
                )for item in order.ordering_item],
            )
            for order in orders
        ]
    )


@router.post(
    "/pre-order",
    description="결제 주문",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_pre_order(
    user: Annotated[ShowUserDocument, Depends(get_current_user)], pre_order_creation_request: PreOrderCreationRequest
) -> PreOrderResponse:
    try:
        order = await pre_order(user, pre_order_creation_request)
    except NoSuchElementException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message},
        )
    return PreOrderResponse(
        user_id=order.user.user_id,
        email=order.email,
        post_code=order.post_code,
        address=order.address,
        detail_address=order.detail_address,
        phone_num=order.phone_num,
        order_name=order.order_name,
        requirements=order.requirements,
        total_price=order.total_price,
    )


@router.post(
    "/create",
    description="결제 주문 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_order(
    user: Annotated[ShowUserDocument, Depends(get_current_user)], order_creation_request: OrderCreationRequest
) -> CreateOrderResponse:
    try:
        order = await create_order(user, order_creation_request)
    except ItemQuantityException as e:
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


@router.post(
    "/payments/{payment_id}",
    description="결제 확인",
    response_class = ORJSONResponse,
    status_code = status.HTTP_200_OK,
)
async def api_find_payment(payment_id: str, user: Annotated[ShowUserDocument, Depends(get_current_user)], payment_request: PaymentRequest) -> int:
    headers = {
        "Authentication": f"PortOne {PORT_ONE_SECRET_KEY}",
    }
    params = {
        "storeId": STORE_ID
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://api.portone.io/payments/{payment_id}", params = params) as res:
            if res.status == "PAID":
                try:
                    return await find_payment(user, payment_request)
                except NoPermissionException as e:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={"message": e.response_message},
                    )
        # 결제 진행중

