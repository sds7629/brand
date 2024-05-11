from bson import ObjectId
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument


async def qna_list() -> list[QnADocument]:
    result = await QnACollection.find_all_qna()
    return result


async def find_qna_by_id(id: ObjectId) -> QnADocument | None:
    result = await QnACollection.find_by_id(id)
    return result


async def find_qna_by_title(title: str) -> list[QnADocument]:
    result = await QnACollection.find_by_title(title)
    return result
