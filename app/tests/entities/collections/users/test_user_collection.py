from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import DeliveryDocument


async def test_유저_회원가입() -> None:
    user_id = "admin1"
    email = "admin@naver.com"
    name = "어드민"
    password = "1234"
    gender = "male"
    phone_num = "010-4444-1322"
    nickname = "admin1"
    delivery_area = [
        DeliveryDocument(
            name="김땡땡",
            post_code="03100",
            address="서울시 종로구 창신동",
            detail_address="지층동",
            recipient_phone="010-0000-1111",
            requirements="빠른 배송 부탁드려요",
        )
    ]

    user = await UserCollection.insert_one(
        user_id, email, name, password, gender, nickname, phone_num, login_method="naver", delivery_area=delivery_area
    )
    results = await UserCollection._collection.find({}).to_list(None)

    assert len(results) == 3
    result = results[0]
    assert result["_id"] == user.id
    assert result["email"] == email
    assert result["name"] == name
    assert result["gender"] == gender
    assert result["nickname"] == nickname


async def test_유저_가져오기() -> None:
    user_id = "admin"

    # user = await UserCollection.find_by_user_id(user_id=user_id)
    user = await UserCollection._collection.find_one({"user_id": user_id})
    assert user is not None
    assert user["user_id"] == user_id
    assert user["email"] == "admin@naver.com"
