from bson import ObjectId

from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.exceptions import QnANotFoundException


async def qna_list() -> list[QnADocument]:
    return await QnACollection.find_all_qna()


async def find_qna_by_id(qna_id: ObjectId) -> QnADocument | None:
    return await QnACollection.find_by_id(qna_id)


async def find_qna_by_title(title: str) -> list[QnADocument]:
    return await QnACollection.find_by_title(title)


async def delete_qna_by_id(qna_id: ObjectId) -> None:
    if not (qna := await QnACollection.find_by_id(qna_id)):
        raise QnANotFoundException(f"No QnA found with id: {id}")

    await QnACollection.delete_by_id(qna_id)
