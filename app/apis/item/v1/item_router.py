import json
from typing import  Sequence

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import ORJSONResponse

from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_response import ItemResponse, OneItemResponse
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.redis_repositories.page_repository import PageRepository
from app.exceptions import (
    ItemNotFoundException,
    NoContentException,
    NoSuchElementException,
    ValidationException,
)
from app.services.item_service import (
    create_item,
    delete_item,
    get_all_item,
    get_item_by_id,
    get_item_by_name,
    updated_item,
)

router = APIRouter(prefix="/v1/items", tags=["items"], redirect_slashes=False)


@router.get(
    "",
    description="모든 아이템정보",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_all_items(name: str | None = None, page: int = 1) -> ItemResponse:
    if name is None:
        item = [
            OneItemResponse(
                id=str(item.id),
                name=item.name,
                price=item.price,
                image_urls=item.image_urls,
                description=item.description,
                registration_date=item.registration_date,
                item_quantity=item.item_quantity,
                size=item.size,
                color=item.color,
                category_codes=item.category_codes,
            )
            for item in await get_all_item(page)
        ]
    else:
        item = [
            OneItemResponse(
                id=str(item.id),
                name=item.name,
                price=item.price,
                image_urls=item.image_urls,
                description=item.description,
                registration_date=item.registration_date,
                item_quantity=item.item_quantity,
                size=item.size,
                color=item.color,
                category_codes=item.category_codes,
            )
            for item in await get_item_by_name(name)
        ]

    return ItemResponse(item=item, page_count=int(await PageRepository.get("item_page_count")))


@router.get(
    "/{item_id}",
    description="상세 아이템 정보",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_one_item(item_id: str) -> OneItemResponse:
    try:
        item = await get_item_by_id(ObjectId(item_id))
    except NoSuchElementException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": e.response_message})
    return OneItemResponse(
        id=str(item.id),
        name=item.name,
        price=item.price,
        image_urls=item.image_urls,
        description=item.description,
        registration_date=item.registration_date,
        item_quantity=item.item_quantity,
        size=item.size,
        color=item.color,
        category_codes=item.category_codes,
        details=item.details,
    )


@router.post(
    "/create",
    description="아이템 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_item(
    item_request: Request,
    item_creation_images: Sequence[UploadFile] = File(...),
) -> OneItemResponse:
    try:
        item_request_form_data = await item_request.form()
        item_data = {key: val for key, val in item_request_form_data.items() if key != "item_creation_images"}
        item_data_to_json = json.loads(item_data["item_creation_request"])
        item_validated_data: ItemCreationRequest = ItemCreationRequest(**item_data_to_json)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)},
        )
    item = await create_item(item_validated_data, item_creation_images)
    return OneItemResponse(
        id=str(item.id),
        name=item.name,
        price=item.price,
        image_urls=item.image_urls,
        description=item.description,
        registration_date=item.registration_date,
        item_quantity=item.item_quantity,
        size=item.size,
        color=item.color,
        details=item.details,
        category_codes=item.category_codes,
    )


@router.put(
    "/{item_id}/update",
    description="아이템 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_item(
        item_id: str,
        item_update_request: Request,
        item_update_images: Sequence[UploadFile] = File(...),
) -> None:
    if item_update_images[0].filename == "":
        item_update_images = None
    try:
        item_update_form = await item_update_request.form()
        item_update_form_to_dict = {key: val for key, val in item_update_form.items() if key != "item_update_images"}
        item_update_json_data = json.loads(item_update_form_to_dict["item_update_request"])
        item_update_validate_data = ItemUpdateRequest(**item_update_json_data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)},
        )
    try:
        await updated_item(ObjectId(item_id), item_update_validate_data, item_update_images)
    except NoContentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": "id should be valid bson object id"}
        )


@router.delete(
    "/{item_id}/delete",
    description="아이템 삭제",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def api_delete_item(item_id: str) -> None:
    try:
        await delete_item(ObjectId(item_id))
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
