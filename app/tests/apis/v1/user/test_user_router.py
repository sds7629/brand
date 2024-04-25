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
        "password": "asdfasdf",
        "gender": "male",
        "nickname": "admin",
    }

    #When
    async with AsyncClient(app = app, base_url = 'http://test') as client:
        response = await client.post(
            "/v1/users/signup",
            json = request_body
        )


    #Then
    print(response)
    assert response.status_code == status.HTTP_200_OK

    user = await UserCollection._collection.find_one({"_id": ObjectId(response.json()['id'])})
    assert user is not None
    assert user["name"] == request_body["name"]
    assert user["nickname"] == request_body["nickname"]