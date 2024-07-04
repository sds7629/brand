import asyncio
import json
from dataclasses import asdict
from typing import Annotated, Sequence, Union

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, UploadFile, File
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.qna.qna_request import QnARequest, UpdateQnARequest
from app.dtos.qna.qna_response import OnlyOneQnAResponse, QnAResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.entities.redis_repositories.page_repository import PageRepository
from app.entities.redis_repositories.view_count_repository import (
    ViewCountRedisRepository,
)
from app.exceptions import NoSuchElementException, QnANotFoundException, ValidationException, NoContentException
from app.services.qna_service import (
    create_qna,
    delete_qna_by_id,
    find_qna_by_id,
    find_qna_by_payload,
    find_qna_by_title,
    find_qna_by_writer,
    qna_list,
    update_qna,
)
from app.utils.cookie_util import CookieUtil
from app.utils.utility import TimeUtil

router = APIRouter(prefix="/v1/qna", tags=["qna"], redirect_slashes=False)


@router.get(
    "",
    description="QnA 게시판",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_qna(
        qna_type: str | None = None,
        keyword: str | None = None,
        page: int = 1
) -> QnAResponse:
    all_qna_data = qna_list(page)

    if qna_type == "title" and keyword is not None:
        all_qna_data = await find_qna_by_title(keyword, page)

    if qna_type == "payload" and keyword is not None:
        all_qna_data = await find_qna_by_payload(keyword, page)

    if qna_type == "writer" and keyword is not None:
        all_qna_data = await find_qna_by_writer(keyword, page)

    qna = [
        OnlyOneQnAResponse(
            id=str(qna.id),
            title=qna.title,
            payload=qna.payload,
            image_urls=qna.image_urls,
            writer=qna.writer.nickname,
            view_count=(
                int(counting)
                if (counting := await ViewCountRedisRepository.get("view_count_" + str(qna.id))) is not None
                else 0
            ),
            is_secret=qna.is_secret,
            is_notice=qna.is_notice,
            created_at=await TimeUtil.get_created_at_from_id(str(qna.id))
        )
        for qna in await all_qna_data
    ]
    return QnAResponse(qna=qna, page_count=int(await PageRepository.get("qna_page_count")))


@router.get(
    "/secret",
    description="QnA 게시판",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_qna(
        user: Annotated[ShowUserDocument, Depends(get_current_user)],
        qna_type: str | None = None,
        keyword: str | None = None,
        page: int = 1
) -> QnAResponse:
    all_secret_qna = await qna_list(page)

    if qna_type == "title" and keyword is not None:
        all_secret_qna = await find_qna_by_title(keyword, page)

    if qna_type == "payload" and keyword is not None:
        all_secret_qna = await find_qna_by_payload(keyword, page)

    if qna_type == "writer" and keyword is not None:
        all_secret_qna = await find_qna_by_writer(keyword, page)

    qna = [
            OnlyOneQnAResponse(
                id=str(qna.id),
                title=qna.title,
                payload=qna.payload,
                image_urls=qna.image_urls,
                writer=qna.writer.nickname,
                view_count=(
                    int(counting)
                    if (counting := await ViewCountRedisRepository.get("view_count_" + str(qna.id))) is not None
                    else 0
                ),
                is_secret=qna.is_secret,
                is_notice=qna.is_notice,
                created_at=await TimeUtil.get_created_at_from_id(str(qna.id))
            )
            for qna in all_secret_qna if (qna.is_secret is False) or (qna.writer == user)
        ]

    return QnAResponse(qna=qna, page_count=int(await PageRepository.get("qna_page_count")))


@router.get(
    "/{qna_id}",
    description="QnA 상세",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_qna_detail(request: Request, response: Response, qna_id: str) -> OnlyOneQnAResponse:
    try:
        result = await find_qna_by_id(ObjectId(qna_id))
    except NoSuchElementException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
    view_count_cookie = await CookieUtil.get_view_count_cookie(request, response)
    if not await ViewCountRedisRepository.is_exist_set(view_count_cookie, qna_id):
        await asyncio.gather(
            ViewCountRedisRepository.increase_data("view_count_" + qna_id),
            ViewCountRedisRepository.add_set(view_count_cookie, qna_id),
        )
    return OnlyOneQnAResponse(
        id=str(result.id),
        title=result.title,
        payload=result.payload,
        writer=result.writer.nickname,
        image_urls=result.image_urls,
        view_count=int(await ViewCountRedisRepository.get("view_count_" + str(result.id))),
        is_secret=result.is_secret,
        is_notice=result.is_notice,
        created_at=await TimeUtil.get_created_at_from_id(str(qna.id))
    )


@router.post(
    "/create",
    description="QnA 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_qna(
        qna_request: Request, user: Annotated[ShowUserDocument, Depends(get_current_user)],
        qna_creation_images: Sequence[UploadFile] = File(default=[])
) -> OnlyOneQnAResponse:
    try:
        qna_request_form_data = await qna_request.form()
        qna_data = {key: val for key, val in qna_request_form_data.items() if key != "qna_creation_images"}
        qna_data_to_json = json.loads(qna_data["qna_creation_request"])
        qna_validate_data = QnARequest(**qna_data_to_json)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)}
        )
    try:
        qna = await create_qna(qna_validate_data, qna_creation_images, user)
        return OnlyOneQnAResponse(
            id=str(qna.id),
            title=qna.title,
            payload=qna.payload,
            writer=qna.writer.nickname,
            image_urls=qna.image_urls,
            view_count=qna.view_count,
            is_notice=qna.is_notice,
            is_secret=qna.is_secret,
            created_at=await TimeUtil.get_created_at_from_id(str(qna.id))
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{qna_id}/delete",
    description="QnA 삭제",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_qna(qna_id: str, user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> None:
    try:
        await delete_qna_by_id(ObjectId(qna_id), user)
    except QnANotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )

    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_422_PRECONDITION,
            detail={"message": "id is not valid"},
        )


@router.put(
    "/{qna_id}/update",
    description="QnA 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_qna(
        qna_id: str,
        qna_request: Request,
        user: Annotated[ShowUserDocument, Depends(get_current_user)],
        qna_update_images: Sequence[UploadFile] = File(default=[]),
) -> None:
    if qna_update_images[0].filename == "":
        qna_update_images = None
    try:
        qna_request_form_data = await qna_request.form()
        qna_data = {key: val for key, val in qna_request_form_data.items() if key != "qna_update_images"}
        qna_data_to_json = json.loads(qna_data["qna_update_request"])
        qna_validate_data = UpdateQnARequest(**qna_data_to_json)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)},
        )
    try:
        await update_qna(ObjectId(qna_id), qna_validate_data, qna_update_images, user)
    except QnANotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
    except NoContentException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.response_message,
        )
