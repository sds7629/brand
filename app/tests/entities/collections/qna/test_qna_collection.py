from bson import ObjectId

from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_collection import UserCollection
from app.services.qna_service import find_qna_by_id, qna_list
from app.utils.utility import TotalUtil


async def test_insert_one() -> None:
    # Given
    user = await UserCollection.find_by_nickname("admin")
    title = "안녕하세요"
    payload = "안녕하세요, 진우입니다ㅡ.ㅡ"
    qna_password = "12343"

    await QnACollection.insert_one(
        title=title,
        payload=payload,
        qna_password=qna_password,
        image_url=None,
        writer=user,
    )

    # When
    result = await QnACollection._collection.find({}).to_list(None)

    # Then
    assert len(result) == 2


async def test_find_by_title() -> None:
    title = "절로가"

    result = await QnACollection.find_by_title(title)

    assert len(result) == 2


async def test_qnq_find_all() -> None:
    result = await qna_list()

    assert len(result) == 2

    assert result[0].title == "안녕하세요"


async def test_qna_find_by_id() -> None:
    find_id = "66458901ac83c88c194b2dca"
    result = await find_qna_by_id(ObjectId(find_id))

    assert result is not None


async def test_delete_by_id() -> None:
    find_id = ObjectId("663cb44edfeda588b0cdf1e3")
    result = await QnACollection.delete_by_id(find_id)

    assert result == 1


async def test_update_by_id() -> None:
    find_id = "66458901ac83c88c194b2dca"
    data = {"payload": "123123"}
    result = await QnACollection.update_by_id(ObjectId(find_id), data)

    assert result > 0
