from typing import Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from app.auth.auth_bearer import get_current_user
from app.dtos.user.user_find_password import EmailSchema
from app.dtos.user.user_profile_response import UserProfileResponse
from app.dtos.user.user_refresh_access_request import RefreshAccessRequest
from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signin_response import Token, UserSigninResponse
from app.dtos.user.user_signout_request import UserSignOutRequest
from app.dtos.user.user_signup_request import UserSignupRequest
from app.dtos.user.user_signup_response import UserSignupResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import UserNotFoundException, ValidationException
from app.services.user_service import (
    delete_user,
    refresh_access_token,
    signin_user,
    signup_user,
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
            delivery_area=user.delivery_area,
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.response_message
        )
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
    except UserNotFoundException as e:
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
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": "id invalid user"})


@router.post(
    "/refresh",
    description="refresh token 사용",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_refresh_access_token(response: Response, refresh_token_request: RefreshAccessRequest) -> Token:
    try:
        token = await refresh_access_token(refresh_token_request)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return Token(
        access_token=token["access_token"],
        refresh_token=refresh_token_request.refresh_token,
    )


@router.post(
    "/find-password",
    description="비밀번호 찾기 - 이메일 전송",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_find_password(data: EmailSchema, background_task: BackgroundTasks) -> None:
    background_task.add_task(find_password_to_email_send, data.email)


@router.post(
    "/set_new_password",
    description="비밀번호 찾기 - 새로운 비밀번호",
     response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_set_new_password():
    ...
