from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_collection import UserCollection
from app.utils.utility import Util
from app.services.qna_service import qna_list, find_qna_by_id
from bson import ObjectId


async def test_insert_one() -> None:
    # Given
    user = await UserCollection.find_by_user_id("admin")
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
    title = "안녕하세요"

    result = await QnACollection.find_by_title(title)

    assert len(result) == 2


async def test_QnA_find_all() -> None:
    result = await qna_list()

    assert len(result) == 2

    assert result[0].title == "안녕하세요"


async def test_QnA_find_by_id() -> None:
    find_id = "663cb269b430f78fdb5f006b"
    result = await find_qna_by_id(ObjectId(find_id))

    assert result is not None
