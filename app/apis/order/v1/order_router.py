from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException

from app.auth.auth_bearer import get_current_user
from app.dtos.item.item_response import OneItemResponse
from app.dtos.user.user_profile_response import UserProfileResponse
from app.entities.collections.users.user_document import ShowUserDocument

from app.dtos.order.order_request import OrderRequest
from app.dtos.order.order_response import OrderResponse, BaseOrderResponse
from app.exceptions import OrderNotFoundException
from app.services.order_service import find_order_user_nickname

router = APIRouter(prefix="/v1/orders", tags=["orders"], redirect_slashes=False)


@router.get(
    "",
    description="유저 주문 정보 가져오기",
    response_class=ORJSONResponse,
    status_code = status.HTTP_200_OK,
)
async def api_get_user_orders(user: Annotated[ShowUserDocument,  Depends(get_current_user)]) -> OrderResponse:
    if user:
        try:
            order_request = OrderRequest(user_nickname = user.nickname)
            order_document = await find_order_user_nickname(order_request)
            order_list = [BaseOrderResponse(
                id = str(order.id),
                ordering_date = order.ordering_date,
                ordering_item = OneItemResponse(
                    id = str(order.ordering_item.id),
                    name = order.ordering_item.name,
                    price = order.ordering_item.price,
                    image_url=order.ordering_item.image_url,
                    description = order.ordering_item.description,
                    registration_date = order.ordering_item.registration_date,
                    item_quantity = order.ordering_item.item_quantity,
                    size = order.ordering_item.size,
                    category_codes = order.ordering_item.category_codes,
                ),
                ordering_item_mount = order.ordering_item_mount,
                ordering_request = order.ordering_request,
                zip_code = order.zip_code,
                address = order.address,
                detail_address = order.detail_address,
                payment_method = order.payment_method,
                total_price = order.total_price,
            ) for order in order_document if order is not None]
            return OrderResponse(order_list = order_list)
        except OrderNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": e.response_message},
            )

# @router.post(
#     "/payment",
#     description="결제 주문",
#     response_class = ORJSONResponse,
#     status_code = status.HTTP_200_OK,
# )
# async def api_payment_order(order_creation_request: OrderCreationRequest) -> None:
#     ...