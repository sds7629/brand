from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_collection import UserCollection
from app.utils.utility import Util




async def test_insert_one() -> None:
    #Given
    user = await UserCollection.find_by_user_id("admin")
    title = "안녕하세요"
    payload = "안녕하세요, 진우입니다ㅡ.ㅡ"
    qna_password = "12343"

    qna = await QnACollection.insert_one(
        title = title,
        payload = payload,
        qna_password = qna_password,
        image_url= None,
        writer = [user],
    )

    #When
    result = await QnACollection._collection.find({}).to_list(None)
    
    #Then
    assert len(result) == 1

