import dataclasses
from typing import  Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.services.qna_service import qna_list, find_qna_by_id
from app.dtos.qna.qna_response import QnAResponse, BeforeQnAResponse
from bson import ObjectId

from pydantic import BaseModel


router = APIRouter(prefix="/v1/qna", tags=["qna"], redirect_slashes=False)


@router.get("", description="QnA 게시판", response_class=ORJSONResponse,)
async def api_get_qna() -> QnAResponse:
    item = [
        BeforeQnAResponse(
            id=str(result.id),
            title=result.title,
            payload=result.payload,
            image_url=result.image_url,
            writer=[result.writer],
        )
        for result in await qna_list()
    ]
    return QnAResponse(qna=item)


# @router.get("/{qna_id}", description="QnA 상세", response_class=ORJSONResponse)
# async def api_get_qna_detail(qna_id: str) -> QnAResponse:
#     try:
#         result = await find_qna_by_id(ObjectId(qna_id))
#         return QnAResponse(
#             id=str(result.id),
#             title=result.title,
#             payload=result.payload,
#             image_url=result.image_url,
#         )
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail={"message": "QnA not found"},
#         )
