from typing import Annotated

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException

from app.auth.auth_bearer import get_current_user
from app.dtos.item.item_response import OneItemResponse
from app.dtos.user.user_profile_response import UserProfileResponse
from app.entities.collections.users.user_document import ShowUserDocument

from app.dtos.order.order_creation_request import OrderCreationRequest
from app.dtos.order.order_request import OrderRequest
from app.dtos.order.order_response import OrderResponse, BaseOrderResponse
from app.exceptions import OrderNotFoundException


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
    status_code=status.HTTP_200_OK,
)
async def api_create_order(user: Annotated[ShowUserDocument, Depends(get_current_user)], order_creation_request: OrderCreationRequest) -> None:
    ...
