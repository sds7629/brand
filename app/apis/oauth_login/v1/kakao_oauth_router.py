import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, RedirectResponse

from app.config import KAKAO_REST_API_KEY

router = APIRouter(prefix="/v1/oauth/kakao", tags=["kakao"], redirect_slashes=False)

REDIRECT_URI = "http://localhost:8080/v1/oauth/kakao/code"


@router.post(
    "",
    description="카카오 로그인",
    response_class=RedirectResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login() -> RedirectResponse:
    response = RedirectResponse(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"
    )

    return response


@router.get(
    "/code",
    description="카카오 코드 발급",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login_with_code(code: str | None = "None") -> None:
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    token_url = f"https://kauth.kakao.com/oauth/token"
    async with aiohttp.ClientSession(headers=headers) as client:
        async with client.post(token_url, data=payload) as res:
            if res.status == 200:
                res_json = await res.json()

    user_headers = {
        "Authorization": f"Bearer {res_json['access_token']}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    async with aiohttp.ClientSession(headers=user_headers) as client:
        async with client.get("https://kapi.kakao.com/v2/user/me") as res:
            if res.status == 200:
                user_data = await res.json()


### 비즈앱 전환 후 이메일 받아서 로그인처리
