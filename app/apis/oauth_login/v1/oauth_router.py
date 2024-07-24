import uuid

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, RedirectResponse

from app.config import KAKAO_REST_API_KEY, NONCE, NAVER_CLIENT_KEY
from app.dtos.oauth_login.kakao_dto import (
    ConfirmIdToken,
    KakaoAccessToken,
    KakaoCode,
    KakaoSignResponse,
)
from app.dtos.oauth_login.naver_dto import NaverSignResponse, NaverCode
from app.exceptions import (
    AuthorizationException,
    UserAlreadyExistException,
    ValidationException,
)
from app.services.oauth_service import confirm_id_token, kakao_login, naver_login

router = APIRouter(prefix="/v1/oauth", tags=["social"], redirect_slashes=False)

REDIRECT_URI = "http://localhost:3000"

nonce = str(uuid.uuid4())


@router.post(
    "/kakao",
    description="카카오 로그인",
    response_class=RedirectResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login() -> RedirectResponse:
    response = RedirectResponse(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}&nonce={NONCE}"
    )

    return response


@router.post(
    "/kakao/login",
    description="카카오 코드 발급",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login_with_code(kakao_code: KakaoCode) -> KakaoSignResponse:
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    payload = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": kakao_code.code,
    }

    token_url = f"https://kauth.kakao.com/oauth/token"

    async with aiohttp.ClientSession(headers=headers) as client:
        async with client.post(token_url, data=payload) as res:
            if res.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"message": "로그인에 실패했습니다. 다시 시도해주세요"},
                )
            res_json = await res.json()
        try:
            await confirm_id_token(ConfirmIdToken(**res_json))
        except AuthorizationException as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": e.response_message})
        try:
            user_data = await kakao_login(KakaoAccessToken(**res_json))
        except AuthorizationException as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": e.response_message})
        except ValidationException as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": e.response_message})

        except UserAlreadyExistException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})

        return KakaoSignResponse(**user_data)


@router.post(
    "/naver",
    description="카카오 로그인",
    response_class=RedirectResponse,
    status_code=status.HTTP_200_OK,
)
async def api_kakao_login() -> RedirectResponse:
    response = RedirectResponse(
        f"https://nid.naver.com/oauth2.0/authorize?state=asdffdsadd&response_type=code&client_id={NAVER_CLIENT_KEY}&redirect_uri=http://localhost:8080/v1/oauth/naver/login")
    return response


@router.post(
    "/naver/login",
    description="네이버 로그인",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_naver_login(naver_code: NaverCode) -> NaverSignResponse:
    try:
        token = await naver_login(naver_code)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": e.response_message},
        )

    except UserAlreadyExistException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message},
        )

    return NaverSignResponse(**token)
