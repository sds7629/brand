import asyncio
import base64
import json
from datetime import datetime
from typing import Any

import aiohttp
from pytz import timezone

from app.config import (
    ACCESS_SECRET_KEY,
    ACCESS_TOKEN_EXFIRE,
    ALGORITHM,
    KAKAO_APP_KEY,
    NAVER_CLIENT_KEY,
    NAVER_SECRET_KEY,
    NONCE,
    REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXFIRE,
)
from app.dtos.oauth_login.kakao_dto import ConfirmIdToken, KakaoAccessToken
from app.dtos.oauth_login.naver_dto import NaverCode
from app.entities.collections import UserCollection
from app.exceptions import (
    AuthorizationException,
    UserAlreadyExistException,
    ValidationException,
)
from app.utils.utility import TotalUtil


async def confirm_id_token(token: ConfirmIdToken) -> None:
    id_token = token.id_token.split(".")
    if len(id_token) != 3:
        raise AuthorizationException(response_message="잘못된 요청입니다.")
    new_id_token = id_token[0] + "." + id_token[1] + "."
    new_id_token = new_id_token + "=" * (4 - len(new_id_token) % 4)
    decoded = base64.b64decode(new_id_token)
    str_token = decoded.decode("utf-8")
    headers, payload, _ = str_token.split("}")
    headers += "}"
    payload += "}"
    json_payload = json.loads(payload)
    now_time = datetime.timestamp(datetime.now(timezone("Asia/Seoul")))

    if json_payload["aud"] != KAKAO_APP_KEY:
        raise AuthorizationException(response_message="잘못된 요청입니다.")

    if json_payload["iss"] != "https://kauth.kakao.com":
        raise AuthorizationException(response_message="잘못된 요청입니다.")

    if json_payload["exp"] <= now_time:
        raise AuthorizationException(response_message="만료된 요청입니다.")

    if json_payload["nonce"] != NONCE:
        raise AuthorizationException(response_message="잘못된 요청입니다.")


async def kakao_login(kakao_token: KakaoAccessToken) -> dict[str, Any]:
    user_profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {kakao_token.access_token}",
    }

    async with aiohttp.ClientSession(headers=headers) as client:
        async with client.get(user_profile_url) as res:
            if res.status != 200:
                raise AuthorizationException(response_message="잘못된 요청입니다.")
            res_json = await res.json()
    profile = res_json["kakao_account"]["profile"]
    user_email = res_json["kakao_account"]["email"]
    user_nickname = profile["nickname"]

    if not (user_email_validate := res_json["kakao_account"]["is_email_valid"]):
        raise ValidationException(response_message="유효하지 않은 이메일입니다. 카카오에 등록된 이메일 인증 바랍니다.")

    user = await UserCollection.find_by_email(user_email)

    if (user is not None) and user.login_method == "카카오":
        access_token, refresh_token = await asyncio.gather(
            TotalUtil.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE),
            TotalUtil.encode(user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE),
        )

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return data

    if (user is not None) and user.login_method != "카카오":
        raise UserAlreadyExistException(response_message=f"{user.login_method}로 이미 가입되어 있습니다!")

    save_user = await UserCollection.social_insert_one(
        email=user_email,
        name=user_nickname,
        nickname=user_nickname,
        is_authenticated=user_email_validate,
        login_method="카카오",
    )

    access_token, refresh_token = await asyncio.gather(
        TotalUtil.encode(save_user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE),
        TotalUtil.encode(save_user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE),
    )

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return data


async def naver_login(naver_code: NaverCode) -> dict[str, Any]:
    access_token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={NAVER_CLIENT_KEY}&client_secret={NAVER_SECRET_KEY}&code={naver_code.code}&state={naver_code.state}"

    async with aiohttp.ClientSession() as client:
        async with client.get(access_token_url) as res:
            response = await res.json()

        access_token = response["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        async with client.get(f"https://openapi.naver.com/v1/nid/me", headers=headers) as res:
            profile_response = await res.json()

            user_data = profile_response["response"]

        user_id = user_data.get("id")
        user_email = user_data.get("email")
        user_phone_number = user_data.get("mobile")
        user_name = user_data.get("name")

        print(user_id, user_email, user_phone_number, user_name)

        if not user_email:
            raise ValidationException(response_message="유효하지 않은 이메일입니다.")

        user = await UserCollection.find_by_email(user_email)

        if (user is not None) and (user.login_method == "네이버"):
            access_token, refresh_token = await asyncio.gather(
                TotalUtil.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE),
                TotalUtil.encode(user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE),
            )

            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            return data

        if (user is not None) and user.login_method != "네이버":
            raise UserAlreadyExistException(response_message=f"{user.login_method}로 가입되어 있습니다")

        save_user = await UserCollection.social_insert_one(
            email=user_email,
            user_id=user_id,
            name=user_name,
            nickname=user_name,
            is_authenticated=True,
            login_method="네이버",
            phone_num=user_phone_number,
        )

        access_token, refresh_token = await asyncio.gather(
            TotalUtil.encode(save_user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE),
            TotalUtil.encode(save_user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE),
        )

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return data
