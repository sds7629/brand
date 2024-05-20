from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.dtos.item.item_response import ItemResponse, OneItemResponse
from app.services.item_service import get_all_item, get_item_by_name

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
