from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import DeliveryDocument


async def test_유저_회원가입() -> None:
    user_id = "admin2"
    email = "admin@naver.com"
    name = "어드민2"
    password = "1234"
    gender = "male"
    phone_num = "010-4444-1322"
    nickname = "admin2"
    delivery_area = [
        DeliveryDocument(
            name="김땡",
            email="admin@naver.com",
            post_code="03100",
            address="서울시 종로구 신동",
            detail_address="3층 102호",
            recipient_phone="010-1111-1111",
            requirements="빠른 배송 부탁드려요",
            is_base_delivery=True,
        )
    ]

    user = await UserCollection.insert_one(
        user_id=user_id,
        email=email,
        name=name,
        password=password,
        nickname=nickname,
        phone_num=phone_num,
        login_method="naver",
        delivery_area=delivery_area,
        is_admin=False,
    )
    results = await UserCollection._collection.find({}).to_list(None)

    assert len(results) == 1
    result = results[0]
    assert result["_id"] == user.id
    assert result["email"] == email
    assert result["name"] == name
    assert result["gender"] == gender
    assert result["nickname"] == nickname


async def test_유저_가져오기() -> None:
    user_id1 = "admin"
    user_id2 = "admin2"

    user1 = await UserCollection.find_by_user_id(user_id=user_id1)
    user2 = await UserCollection.find_by_user_id(user_id=user_id2)
    assert user1 == user2
