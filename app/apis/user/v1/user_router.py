from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from starlette.responses import Response

from app.dtos.user.user_signup_request import UserSignupRequest
from app.dtos.user.user_signup_response import UserSignupResponse
from app.services.user_service import signup_user

router = APIRouter(prefix="/v1/users", tags=["user"], redirect_slashes=False)


@router.post(
    "/signup",
    description="유저 생성",
    response_class=ORJSONResponse,
)
async def api_signup_user(user_signup_request: UserSignupRequest) -> UserSignupResponse:
    user = await signup_user(user_signup_request)
    return UserSignupResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        nickname=user.nickname,
        gender=user.gender,
    )

#
# @router.post(
#     "/signin",
#     description="유저 로그인",
#     response_class=ORJSONResponse,
# )
# async def api_signin_user(user_singin_request: UserSigninRequest) -> UserSigninResponse:
#     user = await signin_user(user_singin_request)
#     ...