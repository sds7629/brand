from bson import ObjectId
from fastapi import status
from httpx import AsyncClient

from app.entities.collections.users.user_collection import UserCollection
from app.main import app


async def test_유저_생성_테스트() -> None:
    request_body = {
        "user_id": "admin",
        "email": "admin@admin.com",
        "name": "admin",
        "password": "1234",
        "gender": "male",
        "nickname": "admin",
        "phone_num": "010-1234-4444",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/signup", json=request_body)

    # Then
    print(response)
    assert response.status_code == status.HTTP_201_CREATED

    user = await UserCollection._collection.find_one({"_id": ObjectId(response.json()["id"])})
    assert user is not None
    assert user["name"] == request_body["name"]
    assert user["nickname"] == request_body["nickname"]


async def test_유저_로그인_테스트() -> None:
    request_body = {
        "user_id": "admin",
        "password": "1234",
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/signin", json=request_body)

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["token"] is not None


async def test_유저_삭제_테스트() -> None:
    request_body = {"base_user_id": "66334733e28ecd65927f0251"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/signout", json=request_body)

    assert response.status_code == status.HTTP_204_NO_CONTENT
