from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.apis.user.v1.user_router import oauth2_scheme
from app.dtos.qna.qna_response import OnlyOneQnAResponse, QnAResponse
from app.exceptions import QnANotFoundException
from app.services.qna_service import delete_qna_by_id, find_qna_by_id, qna_list

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
async def api_get_qna_detail(qna_id: str, token: str = Depends(oauth2_scheme)) -> OnlyOneQnAResponse:
    try:
        result = await find_qna_by_id(ObjectId(qna_id))
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


@router.delete(
    "/{qna_id}/delete",
    description="QnA 삭제",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_qna(qna_id: str) -> None:
    try:
        await delete_qna_by_id(ObjectId(qna_id))

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
