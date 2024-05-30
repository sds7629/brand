from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from app.exceptions import ValidationException

from app.auth.auth_bearer import get_current_user
from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.dtos.cart.cart_response import CartResponse, CartItemResponse
from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.services.cart_service import get_user_carts, create_cart

router = APIRouter(prefix="/v1/cart", tags=["cart"], redirect_slashes=False)


@router.get(
    "",
    description="유저 장바구니",
    response_class = ORJSONResponse,
    status_code = status.HTTP_200_OK,
)
async def api_get_user_carts(user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> Sequence[CartResponse]:
    user_carts = await get_user_carts(user)
    return [
        CartResponse(
            cart_id = str(cart.id),
            items = [
                CartItemResponse(
                    item_id = str(item.id),
                    item_name = item.name,
                    image_url = item.image_url,
                    size = item.size,
                    color = item.color,
                    price = item.price
                )
                for item in cart.items
            ],
            mount = cart.mount,
            total_price = cart.total_price,
        )
        for cart in user_carts if cart is not None
    ]

@router.post(
    "/create",
    description="장바구니 추가",
    response_class = ORJSONResponse,
    status_code = status.HTTP_201_CREATED,
)
async def api_create_cart(user: Annotated[ShowUserDocument, Depends(get_current_user)],cart_creation_request: CartCreationRequest) -> CartResponse:
    try:
        cart = await create_cart(user, cart_creation_request)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )
    return CartResponse(
        cart_id = str(cart.id),
        items=[
            CartItemResponse(
                item_id=str(item.id),
                item_name=item.name,
                image_url=item.image_url,
                size=item.size,
                color=item.color,
                price=item.price
            )
            for item in cart.items
        ],
        mount = cart.mount,
        total_price= cart.total_price,
    )