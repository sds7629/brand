import json
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_current_user
from app.dtos.comment.comment_creation_request import CommentCreationRequest
from app.dtos.comment.comment_response import CommentResponse
from app.dtos.comment.comment_update_request import CommentUpdateRequest
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import (
    NoPermissionException,
    NoSuchContentException,
    ValidationException,
)
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_comments_from_qna,
    get_comments_mount,
    update_comment,
)

router = APIRouter(prefix="/v1/comments", tags=["comments"], redirect_slashes=False)


@router.get(
    "/from-qna/{qna_id}",
    description="QnA Comment",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_comments_from_qna(qna_id: str) -> Sequence[CommentResponse]:
    try:
        comments = await get_comments_from_qna(qna_id)
        mount = await get_comments_mount(qna_id)
    except NoSuchContentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)},
        )
    return [
        CommentResponse(
            writer=comment.writer.name,
            payload=comment.payload,
            image_url=comment.image_url,
            base_qna_id=str(comment.base_qna.id),
            total_qna_mount=mount,
        )
        for comment in comments
    ]


@router.post(
    "/from-qna/create",
    description="QnA Comment Create",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_comment_from_qna(
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    comment_creation_request: CommentCreationRequest,
) -> None:
    try:
        await create_comment(comment_creation_request, user)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)},
        )
    except NoSuchContentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )


@router.put(
    "/{comment_id}",
    description="QnA Comment Update",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_comment(
    comment_id: str,
    user: Annotated[ShowUserDocument, Depends(get_current_user)],
    comment_update_request: CommentUpdateRequest,
) -> None:
    try:
        await update_comment(comment_id, comment_update_request, user)
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message},
        )
    except NoSuchContentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )


@router.delete(
    "/delete/{comment_id}",
    description="QnA Comment Delete",
    response_class=ORJSONResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_comment(comment_id: str, user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> None:
    try:
        await delete_comment(comment_id, user)
    except NoPermissionException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.response_message},
        )
