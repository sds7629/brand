from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

router = APIRouter(prefix="/v1/qna", tags=["qna"], redirect_slashes=False)


@router.get("/qna", description="QnA 게시판", response_class=ORJSONResponse)
async def api_get_qna(): ...
