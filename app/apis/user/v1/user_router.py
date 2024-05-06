from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signin_response import Token, UserSigninResponse
from app.dtos.user.user_signout_request import UserSignOutRequest
from app.dtos.user.user_signup_request import UserSignupRequest
from app.dtos.user.user_signup_response import UserSignupResponse
from app.exceptions import UserNotFoundException
from app.services.user_service import delete_user, signin_user, signup_user

router = APIRouter(prefix="/v1/users", tags=["user"], redirect_slashes=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post(
    "/signup",
    description="유저 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_signup_user(user_signup_request: UserSignupRequest) -> UserSignupResponse:
    user = await signup_user(user_signup_request)
    if user is not None:
        return UserSignupResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            nickname=user.nickname,
            gender=user.gender,
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 요청입니다.")


@router.post(
    "/signin",
    description="유저 로그인",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_signin_user(response: Response, user_signin_request: UserSigninRequest) -> UserSigninResponse:
    user = await signin_user(user_signin_request)
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
            id=str(user["user_data"]["_id"]),
            token=[Token(access_token=user["access_token"], refresh_token=user["refresh_token"])],
            name=user["user_data"]["name"],
            nickname=user["user_data"]["nickname"],
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 요청입니다.")


@router.post(
    "/signout",
    description="유저 탈퇴",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_signout(user_signout_request: UserSignOutRequest) -> None:
    try:
        await delete_user(ObjectId(user_signout_request.base_user_id))
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": "id invalid user"})
