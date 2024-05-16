from typing import Optional

from bson import ObjectId

from app.dtos.qna.qna_request import QnARequest, UpdateQnARequest
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_document import ShowUserDocument
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


async def create_qna(qna_data: QnARequest, user: ShowUserDocument) -> QnADocument:
    return await QnACollection.insert_one(
        title=qna_data.title,
        payload=qna_data.payload,
        image_url=qna_data.image_url,
        qna_password=qna_data.password,
        writer=user,
    )


async def update_qna(qna_id: ObjectId, validate_data: dict[str, str]) -> None:
    if not (qna := await QnACollection.find_by_id(qna_id)):
        raise QnANotFoundException(f"No QnA found with id: {qna_id}")
    await QnACollection.update_by_id(qna_id, validate_data)
