from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_response import ItemResponse, OneItemResponse
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.exceptions import NoContentException
from app.services.item_service import (
    create_item,
    get_all_item,
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
async def api_get_all_items(
    name: str | None = None,
) -> ItemResponse:
    if name is None:
        item = [
            OneItemResponse(
                id=str(item.id),
                name=item.name,
                price=item.price,
                image_url=item.image_url,
                description=item.description,
                registration_date=item.registration_date,
                item_quantity=item.item_quantity,
                size=item.size,
                category_codes=item.category_codes,
            )
            for item in await get_all_item()
        ]
    else:
        item = [
            OneItemResponse(
                id=str(item.id),
                name=item.name,
                price=item.price,
                image_url=item.image_url,
                description=item.description,
                registration_date=item.registration_date,
                item_quantity=item.item_quantity,
                size=item.size,
                category_codes=item.category_codes,
            )
            for item in await get_item_by_name(name)
        ]

    return ItemResponse(item=item)


@router.post(
    "/create",
    description="아이템 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_item(item_creation_request: ItemCreationRequest) -> OneItemResponse:
    item = await create_item(item_creation_request)
    return OneItemResponse(
        id=str(item.id),
        name=item.name,
        price=item.price,
        image_url=item.image_url,
        description=item.description,
        registration_date=item.registration_date,
        item_quantity=item.item_quantity,
        size=item.size,
        category_codes=item.category_codes,
    )


@router.put(
    "/{item_id}/update",
    description="아이템 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def api_update_item(item_id: str, item_update_request: ItemUpdateRequest) -> int:
    try:
        updated_item_count = await updated_item(ObjectId(item_id), item_update_request)
        if updated_item_count > 0:
            return updated_item_count
    except NoContentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": e.response_message})
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"message": "id should be valid bson object id"}
        )
