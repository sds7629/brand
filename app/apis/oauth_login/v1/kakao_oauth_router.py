from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from httpx import AsyncClient

from app.config import KAKAO_REST_API_KEY

router = APIRouter(prefix="/v1/oauth/kakao", tags=["kakao"], redirect_slashes=False)

REDIRECT_URI = "http://localhost:8080/v1/oauth/kakao/code"


@router.post(
    "",
    description="카카오 로그인",
    response_class=RedirectResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login() -> None:
    async with AsyncClient() as client:
        response = await client.get(
            f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"
        )


@router.post(
    "/code",
    description="카카오 코드 발급",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login_with_code(code: str | None = "None") -> None:
    print(code)
