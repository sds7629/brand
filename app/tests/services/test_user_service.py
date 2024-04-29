from httpx import AsyncClient

from app.main import app
from app.services.user_service import signin_user


async def test_유저_로그인_테스트() -> None:
    user = {"user_id": "admin", "password": "1234"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(f"/v1/user/signin", json=user)
