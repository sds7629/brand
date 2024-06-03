from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.dtos.cart.cart_response import CartItemResponse, CartResponse
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import ValidationException
from app.services.cart_service import create_cart, get_user_carts

router = APIRouter(prefix="/v1/cart", tags=["cart"], redirect_slashes=False)


@router.get(
    "",
    description="유저 장바구니",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_carts(user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> Sequence[CartResponse]:
    user_carts = await get_user_carts(user)
    return [
        CartResponse(
            cart_id=str(cart.id),
            item=CartItemResponse(
                item_id=str(cart.item.id),
                item_name=cart.item.name,
                image_url=cart.item.image_url,
                size=cart.item.size,
                color=cart.item.color,
            ),
            quantity=cart.quantity,
            total_price=cart.item.price * cart.quantity,
        )
        for cart in user_carts
        if cart is not None
    ]


@router.post(
    "/create",
    description="장바구니 추가",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_cart(
    user: Annotated[ShowUserDocument, Depends(get_current_user)], cart_creation_request: CartCreationRequest
) -> None:
    try:
        await create_cart(user, cart_creation_request)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )
