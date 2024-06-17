from dataclasses import asdict
from typing import Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.qna.qna_request import QnARequest, UpdateQnARequest
from app.dtos.qna.qna_response import OnlyOneQnAResponse, QnAResponse
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import QnANotFoundException
from app.services.qna_service import (
    create_qna,
    delete_qna_by_id,
    find_qna_by_id,
    qna_list,
    update_qna,
)

router = APIRouter(prefix="/v1/qna", tags=["qna"], redirect_slashes=False)


@router.get(
    "",
    description="QnA 게시판",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_qna() -> QnAResponse:
    item = [
        OnlyOneQnAResponse(
            id=str(result.id),
            title=result.title,
            payload=result.payload,
            image_url=result.image_url,
            writer=result.writer,
        )
        for result in await qna_list()
    ]
    return QnAResponse(qna=item)


@router.get(
    "/{qna_id}",
    description="QnA 상세",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_qna_detail(response: Response, qna_id: str) -> OnlyOneQnAResponse:
    try:
        result = await find_qna_by_id(ObjectId(qna_id))
        response.set_cookie(key = "view_count")
        return OnlyOneQnAResponse(
            id=str(result.id),
            title=result.title,
            payload=result.payload,
            writer=result.writer,
            image_url=result.image_url,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "QnA not found"},
        )


@router.post(
    "/create",
    description="QnA 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_qna(
    qna_request: QnARequest, user: Annotated[ShowUserDocument, Depends(get_current_user)]
) -> OnlyOneQnAResponse:
    try:
        qna = await create_qna(qna_request, user)
        return OnlyOneQnAResponse(
            id=str(qna.id),
            title=qna.title,
            payload=qna.payload,
            writer=qna.writer,
            image_url=qna.image_url,
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
    qna_id: str, qna_request: UpdateQnARequest, user: Annotated[ShowUserDocument, Depends(get_current_user)]
) -> None:
    qna = {key: val for key, val in asdict(qna_request).items() if val is not None}
    if len(qna) >= 1:
        try:
            await update_qna(ObjectId(qna_id), qna, user)
        except QnANotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": e.response_message},
            )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "QnA Validation Error"})
