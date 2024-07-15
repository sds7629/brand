import functools
import json
from datetime import timedelta
from typing import Callable

from app.utils.redis_ import redis
from requests_futures.sessions import FuturesSession

CACHE_TTL = timedelta(days=7)


async def cached(func) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        key = f"kakao_oidc_open_keys"
        value = await redis.get(key)
        if value:
            return json.loads(value)
        else:
            result = func(*args, **kwargs)
            await redis.set(key, json.dumps(result), ex=CACHE_TTL.total_seconds())
            return result

    return wrapper


class KakaoOauthClient:
    def __init__(self):
        self.session = FuturesSession()
        self.base_url = "https://kauth.kakao.com"

    @cached
    async def get_kakao_oidc_open_keys(self) -> dict:
        url = f"{self.base_url}/.well-known/jwks.json"
        response = self.session.get(url)
        return response.result().json()
