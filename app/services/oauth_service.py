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
    NONCE,
    REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXFIRE,
)
from app.dtos.oauth_login.kakao_dto import ConfirmIdToken, KakaoAccessToken
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
    print(kakao_token.access_token)
    async with aiohttp.ClientSession(headers=headers) as client:
        async with client.get(user_profile_url) as res:
            if res.status != 200:
                raise AuthorizationException(response_message="잘못된 요청입니다.")
            res_json = await res.json()
    profile = res_json["kakao_account"]["profile"]
    user_email = res_json["kakao_account"]["email"]
    user_nickname = profile["nickname"]

    if user := await UserCollection.find_by_email(user_email) is not None:
        raise UserAlreadyExistException(response_message=f"{user.login_method}로 이미 가입되어 있습니다!")

    if not (user_email_validate := res_json["kakao_account"]["is_email_valid"]):
        raise ValidationException(response_message="유효하지 않은 이메일입니다.")

    save_user = await UserCollection.social_insert_one(
        email=user_email,
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
