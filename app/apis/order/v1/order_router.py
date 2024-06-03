from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException

from app.auth.auth_bearer import get_current_user
from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.users.user_document import ShowUserDocument



from app.dtos.order.order_creation_request import OrderCreationRequest
from app.dtos.order.order_request import OrderRequest
from app.dtos.order.order_response import OrderResponse, BaseOrderResponse
from app.exceptions import OrderNotFoundException, NoSuchElementException
from app.services.order_service import create_order

router = APIRouter(prefix="/v1/orders", tags=["orders"], redirect_slashes=False)


@router.get(
    "",
    description="유저 주문 정보 가져오기",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_orders(user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> OrderResponse:
    ## 수정 예정
    ...


@router.post(
    "/create",
    description="결제 주문",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_order(user: Annotated[ShowUserDocument, Depends(get_current_user)], order_creation_request: OrderCreationRequest) -> BaseOrderResponse:
    try:
        order = await create_order(user, order_creation_request)
    except NoSuchElementException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
    return BaseOrderResponse(
        id = str(order.id),
        user_id = order.user.user_id,
        merchant_id = order.merchant_id,
        post_code = order.post_code,
        address = order.address,
        detail_address = order.detail_address,
        orderer_name = order.orderer_name,
        phone_num=order.phone_num,
        requirements = order.requirements,
        payment_method=order.payment_method,
        ordering_date = order.ordering_date,
        is_payment = order.is_payment,
    )