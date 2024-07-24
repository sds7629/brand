from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.payment.payment_request import PaymentRequest, SetPaymentRequest, FailPaymentRequest
from app.dtos.payment.payment_response import PaymentHistoryResponse, FailPaymentResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NoSuchContentException, ValidationException
from app.services.payment_service import get_history, set_payment, success_payment, fail_payment
from app.utils.utility import TimeUtil

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"detail": str(e)})

    return [
        PaymentHistoryResponse(
            merchant_id=history.merchant_id,
            payment_name=history.payment_name,
            total_price=history.total_price,
            payment_time=history.payment_time,
            payment_method=history.payment_method,
            payment_status="결제 완료" if history.payment_status is True else "결제 실패"
        )
        for history in histories
    ]


@router.post(
    "/toss",
    description="결제 데이터 임시 저장",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED
)
async def api_set_payment(
        user: Annotated[ShowUserDocument, Depends(get_current_user)],
        set_payment_request: SetPaymentRequest,
) -> None:
    try:
        result = await set_payment(user, set_payment_request)
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"detail": e.response_message},
        )


@router.get(
    "/success",
    description="결제 성공",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_success_payment(
        amount: int,
        payment_key: str | None = Query(None, alias="paymentKey"),
        payment_type: str | None = Query(None, alias="paymentType"),
        order_id: str | None = Query(None, alias="orderId"),
) -> None:
    try:
        payment_request = PaymentRequest(
            amount=amount,
            payment_key=payment_key,
            payment_type=payment_type,
            order_id=order_id,
        )
        await success_payment(payment_request)
    except NoSuchContentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message}
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message}
        )

    return


@router.get(
    "/fail",
    description="결제 실패",
    response_class=ORJSONResponse,
    status_code=status.HTTP_404_NOT_FOUND,
)
async def api_fail_payment(
        code: str,
        message: str,
        order_id: str | None = Query(None, alias="orderId"),
) -> FailPaymentResponse:
    try:
        validate_data = FailPaymentRequest(code, message, order_id)
        await fail_payment(validate_data)
    except NoSuchContentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message}
        )
    return FailPaymentResponse(
        code=code,
        message=message,
        merchant_id=order_id
    )
