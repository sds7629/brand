import asyncio

from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import UserDocument


async def test_유저_회원가입() -> None:
    user_id = "admin"
    email = "admin@naver.com"
    name = "어드민"
    password = "1234"
    gender = "male"
    nickname = "admin"

    user = await UserCollection.insert_one(user_id, email, password, name, gender, nickname)
    results = await UserCollection._collection.find({}).to_list(None)

    assert len(results) == 1
    result = results[0]
    assert result["_id"] == user.id
    assert result["email"] == email
    assert result["name"] == name
    assert result["gender"] == gender
    assert result["nickname"] == nickname
