import json
from typing import Sequence

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import ORJSONResponse

from app.auth.auth_bearer import get_admin_user
from app.dtos.item.item_creation_request import (
    FitSizing,
    ItemCreationRequest,
    ItemOptions,
)
from app.dtos.item.item_response import ItemResponse, OneItemResponse
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.redis_repositories.page_repository import PageRepository
from app.exceptions import (
    NoSuchContentException,
    NotFoundException,
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
        items = await get_all_item(page)
    else:
        items = await get_item_by_name(name)

    item = [
        OneItemResponse(
            id=str(item.id),
            name=item.name,
            price=item.price,
            image_urls=item.image_urls,
            description=item.description,
            options=item.options,
            item_details_menu=item.item_detail_menu,
            registration_date=item.registration_date,
            category_codes=item.category_codes,
        )
        for item in items
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
    except NoSuchContentException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": e.response_message})
    return OneItemResponse(
        id=str(item.id),
        name=item.name,
        price=item.price,
        image_urls=item.image_urls,
        description=item.description,
        options=item.options,
        item_details_menu=item.item_detail_menu,
        registration_date=item.registration_date,
        category_codes=item.category_codes,
    )


@router.post(
    "/create",
    description="아이템 생성",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_admin_user)],
)
async def api_create_item(
    item_request: Request,
    item_creation_images: Sequence[UploadFile] = File(...),
) -> OneItemResponse:
    try:
        item_request_form_data = await item_request.form()
        item_data = {key: val for key, val in item_request_form_data.items() if key != "item_creation_images"}
        item_data_to_json = json.loads(item_data["item_creation_request"])
        item_validated_data: ItemCreationRequest = ItemCreationRequest(
            name=item_data_to_json["name"],
            price=item_data_to_json["price"],
            description=item_data_to_json["description"],
            details=item_data_to_json["details"],
            fit_sizing=FitSizing(**item_data_to_json["fit_sizing"]),
            options=[ItemOptions(**items) for items in item_data_to_json["options"]],
            fabric=item_data_to_json["fabric"],
            category=item_data_to_json["category"],
        )

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
        options=item.options,
        item_details_menu=item.item_detail_menu,
        registration_date=item.registration_date,
        category_codes=item.category_codes,
    )


@router.put(
    "/{item_id}/update",
    description="아이템 수정",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_admin_user)],
)
async def api_update_item(
    item_id: str,
    item_update_request: Request,
    item_update_images: Sequence[UploadFile] = File(default=None),
) -> None:
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
    except NoSuchContentException as e:
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
    dependencies=[Depends(get_admin_user)],
)
async def api_delete_item(item_id: str) -> None:
    try:
        await delete_item(ObjectId(item_id))
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.response_message},
        )
