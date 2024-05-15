from httpx import AsyncClient

from app.config import ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE
from app.entities.collections import UserCollection
from app.main import app
from app.services.user_service import get_current_user
from app.utils.utility import Util


async def test_유저_로그인_테스트() -> None:
    user = {"user_id": "admin", "password": "1234"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(f"/v1/user/signin", json=user)


async def test_현재_유저_테스트() -> None:
    user = await UserCollection.find_by_user_id("admin")
    user_jwt_token = await Util.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE)

    result = await get_current_user(user_jwt_token)

    assert result.user_id == "admin"
