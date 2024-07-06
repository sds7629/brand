from dataclasses import asdict
from datetime import datetime
from typing import Any, Sequence

from bson import ObjectId
from fastapi import UploadFile

from app.dtos.qna.qna_request import QnARequest, UpdateQnARequest
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    NoPermissionException,
    NoSuchContentException,
    NotFoundException,
)
from app.utils.connection_aws import upload_image


async def qna_list(page: int) -> list[QnADocument]:
    offset = (page - 1) * 15
    return await QnACollection.find_all_qna(offset)


async def find_qna_by_id(qna_id: ObjectId) -> QnADocument | None:
    if (qna := await QnACollection.find_by_id(qna_id)) is None:
        raise NoSuchContentException(response_message="QnA를 찾을 수 없습니다.")
    return qna


async def find_qna_by_title(keyword: str, page: int) -> Sequence[QnADocument]:
    offset = (page - 1) * 15
    filtering_item = await QnACollection.find_by_title(keyword, offset)
    return filtering_item


async def find_qna_by_payload(keyword: str, page: int) -> Sequence[QnADocument]:
    offset = (page - 1) * 15
    filtering_item = await QnACollection.find_by_payload(keyword, offset)
    return filtering_item


async def find_qna_by_writer(keyword: str, page: int) -> Sequence[QnADocument]:
    offset = (page - 1) * 15
    filtering_item = await QnACollection.find_by_writer(keyword, offset)
    return filtering_item


async def delete_qna_by_id(qna_id: ObjectId, user: ShowUserDocument) -> None:
    if not (qna := await QnACollection.find_by_id(qna_id)):
        raise NotFoundException(f"No QnA found with id: {id}")

    if qna.writer.user_id != user.user_id:
        raise NoPermissionException(response_message="작성자가 아닙니다.")

    await QnACollection.delete_by_id(qna_id)


async def create_qna(
    qna_data: QnARequest, qna_creation_images: Sequence[UploadFile], user: ShowUserDocument
) -> QnADocument:
    qna_creation_image_urls_from_aws = []
    if bool(qna_creation_images):
        qna_creation_image_urls_from_aws = [
            (await upload_image(image))["url"] for image in qna_creation_images if image.filename != ""
        ]
    return await QnACollection.insert_one(
        title=qna_data.title,
        payload=qna_data.payload,
        image_urls=qna_creation_image_urls_from_aws,
        is_secret=qna_data.is_secret,
        writer=user,
    )


async def update_qna(
    qna_id: ObjectId,
    validate_data: UpdateQnARequest,
    qna_update_images: Sequence[UploadFile] | None,
    user: ShowUserDocument,
) -> None:
    if not (qna := await QnACollection.find_by_id(qna_id)):
        raise NotFoundException(f"No QnA found with id: {qna_id}")

    if qna.writer.user_id != user.user_id:
        raise NoPermissionException(response_message="작성자가 아닙니다.")

    if len(data := {key: val for key, val in asdict(validate_data).items() if val is not None}) > 0:
        if bool(qna_update_images):
            item_update_image_urls_from_aws = [
                (await upload_image(image))["url"] for image in qna_update_images if image.filename != ""
            ]
            data["image_urls"] = item_update_image_urls_from_aws
        updated_item_count = await QnACollection.update_by_id(qna_id, data)
    else:
        raise NoSuchContentException(response_message="No Content")
