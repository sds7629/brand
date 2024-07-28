from dataclasses import asdict
from typing import Sequence
from bson import ObjectId

from app.dtos.notice.notice_request import NoticeRequest, UpdateNoticeRequest
from app.entities.collections import NoticeCollection
from app.entities.collections.notice.notice_document import NoticeDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NotFoundException, NoPermissionException, ValidationException


async def get_notices(page: int) -> Sequence[NoticeDocument]:
    offset = (page - 1) * 15
    notice_list = await NoticeCollection.find_all_notice(offset)
    return notice_list


async def create_notice(
        user: ShowUserDocument,
        notice_request: NoticeRequest,
) -> NoticeDocument:
    notice = await NoticeCollection.insert_one(
        title=notice_request.title,
        payload=notice_request.payload,
        writer=user
    )

    return notice


async def update_notice(
        notice_id: str,
        user: ShowUserDocument,
        update_notice_request: UpdateNoticeRequest,
) -> int:
    if not (notice := await NoticeCollection.find_by_id(ObjectId(notice_id))):
        raise NotFoundException(response_message="공지가 없어요")

    if notice.writer != user:
        raise NoPermissionException(response_message="권한이 없습니다.")

    if len(data := {key: val for key, val in asdict(update_notice_request).items() if val is not None}) == 0:
        raise ValidationException(response_message="업데이트할 데이터가 없습니다.")

    update_mount = await NoticeCollection.update_by_id(
        notice_id=ObjectId(notice_id),
        data=data
    )

    return update_mount


async def delete_notice(user: ShowUserDocument, notice_id: str) -> int:
    if (notice := await NoticeCollection.find_by_id(ObjectId(notice_id))) is None:
        raise NotFoundException(response_message="공지가 없어요")

    if notice.writer != user:
        raise NoPermissionException(response_message="권한이 없습니다.")

    result = await NoticeCollection.delete_by_id(notice_id=ObjectId(notice_id))

    return result
