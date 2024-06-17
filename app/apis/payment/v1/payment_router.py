from typing import Annotated, Sequence

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.config import PORT_ONE_SECRET_KEY, STORE_ID
from app.dtos.payment.payment_request import PaymentRequest
from app.dtos.payment.payment_response import PaymentHistoryResponse, PaymentResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NoSuchElementException
from app.services.payment_service import find_payment, get_history

router = APIRouter(prefix="/v1/payment", tags=["Payment"], redirect_slashes=False)


@router.get(
    "/history",
    description="유저 결제 내역 확인",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_history(
    user: Annotated[ShowUserDocument, Depends(get_current_user)]
) -> Sequence[PaymentHistoryResponse]:
    try:
        histories = await get_history(user)
    except NoSuchElementException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"detail": e.response_message})

    return [
        PaymentHistoryResponse(
            order=str(history.order),
            item_name=[item.name for item in history.items],
            total_price=history.total_price,
            payment_time=history.payment_time,
        )
        for history in histories
    ]


@router.post(
    "/{payment_id}",
    description="결제 확인",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_find_payment(
    payment_id: str, user: Annotated[ShowUserDocument, Depends(get_current_user)], payment_request: PaymentRequest
) -> PaymentResponse:
    headers = {
        "Authentication": f"PortOne {PORT_ONE_SECRET_KEY}",
    }
    params = {"storeId": STORE_ID}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://api.portone.io/payments/{payment_id}", params=params) as res:
            if res.status == "PAID":
                try:
                    result = await find_payment(user, payment_request)
                    if result[1] >= 1:
                        return PaymentResponse(
                            user_name=result[0].user.name,
                            item_name=[item.name for item in result[0].items],
                            total_price=result[0].total_price,
                        )
                except NoPermissionException as e:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={"message": e.response_message},
                    )
