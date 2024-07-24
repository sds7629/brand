from dataclasses import asdict
from typing import Sequence

from bson import ObjectId
from fastapi import UploadFile

from app.dtos.comment.comment_creation_request import CommentCreationRequest
from app.dtos.comment.comment_update_request import CommentUpdateRequest
from app.entities.collections import QnACollection
from app.entities.collections.comments.comment_collection import CommentCollection
from app.entities.collections.comments.comment_document import CommentDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NoPermissionException, NoSuchContentException
from app.utils.connection_aws import upload_image


async def get_comments_from_qna(qna_id: str) -> Sequence[CommentDocument | None]:
    comments = await CommentCollection.find_by_base_qna(ObjectId(qna_id))
    return comments


async def get_comments_mount(qna_id: str) -> int:
    mount = await CommentCollection.get_all_comment_from_qna(ObjectId(qna_id))
    return mount


async def create_comment(
    comment_creation_data: CommentCreationRequest,
    writer: ShowUserDocument,
) -> CommentDocument:

    if (base_qna := await QnACollection.find_by_id(ObjectId(comment_creation_data.base_qna))) is None:
        raise NoSuchContentException(response_message="Not found")

    return await CommentCollection.insert_one(
        writer=writer,
        payload=comment_creation_data.payload,
        base_qna=base_qna,
    )


async def update_comment(
    comment_id: str,
    comment_update_data: CommentUpdateRequest,
    writer: ShowUserDocument,
) -> int:
    comment = await CommentCollection.find_by_id(ObjectId(comment_id))

    if comment.writer != writer:
        raise NoPermissionException("접근 권한이 없습니다.")

    if len(data := {key: val for key, val in asdict(comment_update_data).items() if val is not None}):
        updated_comment_count = await CommentCollection.update_by_id(ObjectId(comment_id), data)
        return updated_comment_count

    raise NoSuchContentException(response_message="No Contents")


async def delete_comment(comment_id: str, user: ShowUserDocument) -> None:
    comment = await CommentCollection.find_by_id(ObjectId(comment_id))
    if comment.writer != user:
        raise NoPermissionException(response_message="권한이 없습니다.")
    await CommentCollection.delete_by_id(ObjectId(comment_id))
