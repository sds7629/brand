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
    request_body = {"user_id": "admin2", "password": "1234"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/signin", json=request_body)

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["token"] is not None


async def test_유저_삭제_테스트() -> None:
    request_body = {"base_user_id": "66334733e28ecd65927f0251"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/signout", json=request_body)

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_유저_마이페이지() -> None:
    header = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjNjYjI0M2UzNjkzNTY0YTE1MGZjNjkiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNTc3NTY0N30.pvpXIHoBWhwGrQoxqwOsq3LSVY9_38vudLXZ2WYlcqI"
    }
    async with AsyncClient(app=app, base_url="http://test", headers=header) as client:
        response = await client.get("/v1/users/me")

        assert response.status_code == status.HTTP_200_OK


async def test_리프레시_토큰() -> None:
    request_body = {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2Njc4MDBmODBjZDE2MDZhMzNlODFjNDciLCJ1c2VyX2lkIjoiYWRtaW4yIiwibmlja25hbWUiOiJhZG1pbjIiLCJleHAiOjE3MTkxNTE2MzV9.vXaN1RP-bbmmibxBEYfmZNsiBz_qdS7fj3PMQr6vxvU"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/users/refresh", json=request_body)

        assert response.status_code == status.HTTP_200_OK


async def test_닉네임_중복() -> None:
    request_body = {"nickname": "admin"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/users/check?email=admin")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["result"] == "is_duplicated"
