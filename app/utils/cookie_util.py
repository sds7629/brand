from uuid import uuid4
from fastapi import Response, Request
class CookieUtil:

    @classmethod
    async def get_view_count_cookie(cls, request: Request) -> ...:
        cookies = request.cookies["view_count"]
        if cookies is None:
            return cookies


    @classmethod
    async def create_cookies(cls) -> ...:
        ...
    # 쿠키 만들기 진행중