from typing import Annotated, Sequence

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.cart.cart_creation_request import OneCartCreationRequest
from app.dtos.cart.cart_response import (
    CartCreationResponse,
    CartItemResponse,
    CartResponse,
)
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, ValidationException
from app.services.cart_service import create_cart, delete_cart, get_user_carts

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
                image_urls=cart.item.image_urls,
            ),
            quantity=cart.quantity,
            options=cart.options,
            total_price=cart.total_price,
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
    user: Annotated[ShowUserDocument, Depends(get_current_user)], cart_creation_request: OneCartCreationRequest
) -> CartCreationResponse:
    try:
        cart_id_list = await create_cart(user, cart_creation_request)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )
    return CartCreationResponse(cart_id=[str(cart.id) for cart in cart_id_list])


@router.delete(
    "{cart_id}/delete",
    description="장바구니 삭제",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_cart(user: Annotated[ShowUserDocument, Depends(get_current_user)], cart_id: str) -> None:
    try:
        await delete_cart(user, ObjectId(cart_id))
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message},
        )
