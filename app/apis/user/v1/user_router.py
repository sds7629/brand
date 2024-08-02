from dataclasses import asdict
from typing import Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from app.auth.auth_bearer import get_current_user
from app.dtos.user.user_delivery_request import DeliveryRequest, UpdateDeliveryRequest
from app.dtos.user.user_duplicated_request import DuplicatedRequest
from app.dtos.user.user_duplicated_response import DuplicatedResponse
from app.dtos.user.user_find_password import EmailSchema
from app.dtos.user.user_profile_response import DeliveryResponse, UserProfileResponse
from app.dtos.user.user_refresh_access_request import RefreshAccessRequest
from app.dtos.user.user_set_passwd_request import UserSetPasswdRequest
from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signin_response import Token, UserSigninResponse
from app.dtos.user.user_signout_request import UserSignOutRequest
from app.dtos.user.user_signup_request import UserSignupRequest
from app.dtos.user.user_signup_response import UserSignupResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NotFoundException, ValidationException
from app.services.user_service import (
    check_nickname_or_email,
    delete_delivery,
    delete_user,
    refresh_access_token,
    set_delivery,
    signin_user,
    signup_user,
    update_delivery,
)
from app.utils.send_mail import find_password_to_email_send

router = APIRouter(
    prefix="/v1/users",
    tags=["user"],
    redirect_slashes=False,
)

oauth2_scheme = OAuth2PasswordBearer("v1/users/signin")


@router.get(
    "/me",
    description="유저 마이페이지",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_profile(user: Annotated[ShowUserDocument, Depends(get_current_user)]):
    if user:
        return UserProfileResponse(
            id=str(user.id),
            name=user.name,
            nickname=user.nickname,
            email=user.email,
            delivery_area=[
                DeliveryResponse(
                    id=str(area.id),
                    name=area.name,
                    email=area.email,
                    post_code=area.post_code,
                    address=area.address,
                    detail_address=area.detail_address,
                    recipient_phone=area.recipient_phone,
                    requirements=area.requirements,
                    is_base_delivery=area.is_base_delivery,
                )
                for area in user.delivery_area
            ],
        )


@router.post(
    "/signup",
    description="유저 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_signup_user(user_signup_request: UserSignupRequest) -> UserSignupResponse:
    try:
        user = await signup_user(user_signup_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response_message)
    if user is not None:
        return UserSignupResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            nickname=user.nickname,
        )


@router.post(
    "/signin",
    description="유저 로그인",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_signin_user(response: Response, user_signin_request: UserSigninRequest) -> UserSigninResponse:
    try:
        user = await signin_user(user_signin_request)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.response_message,
        )
    if user is not None:
        response.set_cookie(
            key="access_token",
            value=user["access_token"],
            secure=True,
            httponly=True,
            samesite="lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=user["refresh_token"],
            secure=True,
            httponly=True,
            samesite="lax",
        )
        return UserSigninResponse(
            id=str(user["user_data"].id),
            token=[Token(access_token=user["access_token"], refresh_token=user["refresh_token"])],
            name=user["user_data"].name,
            nickname=user["user_data"].nickname,
        )


@router.post(
    "/logout",
    description="유저 로그아웃",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(oauth2_scheme)],
)
async def api_logout_user(response: Response) -> None:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")


@router.post(
    "/signout",
    description="유저 탈퇴",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_signout(
    user: Annotated[ShowUserDocument, Depends(get_current_user)], user_signout_request: UserSignOutRequest
) -> None:
    try:
        await delete_user(user, ObjectId(user_signout_request.base_user_id))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": "id invalid user"})


@router.post(
    "/refresh",
    description="refresh token",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_refresh_access_token(response: Response, refresh_token_request: RefreshAccessRequest) -> Token:
    try:
        token = await refresh_access_token(refresh_token_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": e.response_message})

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        secure=True,
        httponly=True,
        samesite="lax",
        domain="localhost",
    )

    return Token(
        access_token=token["access_token"],
        refresh_token=refresh_token_request.refresh_token,
    )


@router.post(
    "/check",
    description="닉네임, 이메일 중복 체크",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_check_nickname(nickname_or_email_request: DuplicatedRequest) -> DuplicatedResponse:
    try:
        result = await check_nickname_or_email(nickname_or_email_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response_message)
    return DuplicatedResponse(result=result)


@router.post("/set-delivery", description="배송지 추가", response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def api_set_delivery(
    user: Annotated[ShowUserDocument, Depends(get_current_user)], delivery_request: DeliveryRequest
) -> None:
    try:
        await set_delivery(user, delivery_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response_message)


@router.put(
    "/delivery/update/{delivery_id}",
    description="배송지 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_delivery(
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    delivery_id: str,
    update_delivery_request: UpdateDeliveryRequest,
) -> None:
    try:
        await update_delivery(user, delivery_id, update_delivery_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response_message)


@router.delete(
    "/delivery/delete/{delivery_id}",
    description="배송지 삭제",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_delivery(
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    delivery_id: str,
) -> None:
    try:
        await delete_delivery(user, delivery_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/find-password",
    description="비밀번호 찾기 - 이메일 전송",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_find_password(data: EmailSchema, background_task: BackgroundTasks) -> None:
    background_task.add_task(find_password_to_email_send, data.email)


@router.post(
    "/set_newpassword",
    description="비밀번호 찾기 - 새로운 비밀번호 설정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_set_new_password(user_set_passwd_request: UserSetPasswdRequest) -> None:
    # result = await set_new_password(user_set_passwd_request)
    ...
