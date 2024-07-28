from typing import Sequence, Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import ORJSONResponse

from app.dtos.notice.notice_request import NoticeRequest, UpdateNoticeRequest
from app.dtos.notice.notice_response import NoticeResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import NotFoundException, NoPermissionException, ValidationException
from app.services.notice_service import get_notices, create_notice, update_notice, delete_notice
from app.auth.auth_bearer import get_admin_user
from app.utils.utility import TimeUtil

router = APIRouter(prefix="/v1/notice", tags=["Notice"], redirect_slashes=False)


@router.get(
    "",
    description="공지사항 가져오기",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_notices(page: int = 1) -> Sequence[NoticeResponse]:
    try:
        notice_list = await get_notices(page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return [
        NoticeResponse(
            notice_id=str(notice.id),
            title=notice.title,
            payload=notice.payload,
            created_at=await TimeUtil.get_created_at_from_id(str(notice.id)),
            admin_nickname=notice.writer.nickname,
        )
        for notice in notice_list
    ]


@router.post(
    "/create",
    description="공지사항 작성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_notice(
        user: Annotated[ShowUserDocument, Depends(get_admin_user)],
        notice_request: NoticeRequest
) -> None:
    try:
        await create_notice(user, notice_request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/update/{notice_id}",
    description="공지사항 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_notice(
        notice_id: str,
        user: Annotated[ShowUserDocument, Depends(get_admin_user)],
        update_request: UpdateNoticeRequest
) -> None:
    try:
        result = await update_notice(notice_id, user, update_request)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message}
        )
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message}
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.response_message}
        )


@router.delete(
    "/delete/{notice_id}",
    description="공지 삭제",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_notice(
        user: Annotated[ShowUserDocument, Depends(get_admin_user)],
        notice_id: str
) -> None:
    try:
        await delete_notice(user, notice_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message}
        )
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message}
        )

