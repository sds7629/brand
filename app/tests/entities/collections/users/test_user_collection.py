import asyncio

from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import UserDocument


async def test_유저_회원가입() -> None:
    user_id = "sds7629"
    email = "sds7629@naver.com"
    name = "김진우"
    password = "rlawlsdn1!"
    gender = "male"
    nickname = "jinoo"

    user = await UserCollection.insert_one(user_id, email, password, name, gender, nickname)
    results = await UserCollection._collection.find({}).to_list(None)

    assert len(results) == 1
    result = results[0]
    assert result["_id"] == user.id
    assert result["email"] == email
    assert result["name"] == name
    assert result["gender"] == gender
    assert result["nickname"] == nickname
