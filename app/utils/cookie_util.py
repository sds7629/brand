from datetime import datetime, time, timedelta
from uuid import uuid4

from fastapi import Request, Response

from app.utils.utility import TimeUtil


class CookieUtil:

    @classmethod
    async def get_view_count_cookie(cls, request: Request, response: Response) -> str:
        cookies = request.cookies.get("view_count")
        if cookies is None:
            cookies = await cls.create_cookies(response)
        return cookies

    @classmethod
    async def create_cookies(cls, response: Response) -> str:
        user_cookie_uuid = uuid4()

        midnight_seconds, next_midnight = await TimeUtil.to_midnight_seconds()

        response.set_cookie(key="view_count", value=str(user_cookie_uuid), httponly=True, expires=midnight_seconds)

        return str(user_cookie_uuid)
