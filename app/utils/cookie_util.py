from datetime import datetime, time, timedelta
from uuid import uuid4
from fastapi import Response, Request


class CookieUtil:

    @classmethod
    async def get_view_count_cookie(cls, request: Request, response: Response) -> str:
        cookies = request.cookies["view_count"]
        if cookies is None:
            await cls.create_cookies(response)
        return cookies

    @classmethod
    async def create_cookies(cls, response: Response) -> None:
        user_cookie_uuid = uuid4()

        now = datetime.utcnow()

        if now.time() > time(0, 0):
            next_midnight = datetime.combine(now.date() + timedelta(days=1), time(0, 0))
        else:
            next_midnight = datetime.combine(now.date(), time(0, 0))

        response.set_cookie(key="view_count", value=str(user_cookie_uuid), httponly=True, expires=next_midnight)

