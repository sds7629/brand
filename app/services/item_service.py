from dataclasses import asdict
from typing import Sequence, Any

from bson import ObjectId
from fastapi import File, UploadFile

from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.collections.items.item_collection import ItemCollection
from app.entities.collections.items.item_document import ItemDocument
from app.exceptions import (
    ItemNotFoundException,
    NoContentException,
    NoSuchElementException,
)
from app.utils.connection_aws import upload_image


async def create_item(
    item_creation_request: ItemCreationRequest, item_creation_images: Sequence[UploadFile] = File(...)
) -> ItemDocument:
    if bool(item_creation_images):
        item_creation_image_urls_from_aws = [(await upload_image(image))["url"] for image in item_creation_images]
    options_list = [asdict(option).values() for option in item_creation_request.options]
    options = {
        key: val for key, val in options_list if val is not None
    }
    details = {
        f"detail-{i+1}": item_creation_request.details[i] for i in range(len(item_creation_request.details))
    }
    item = await ItemCollection.insert_one(
        name=item_creation_request.name,
        price=item_creation_request.price,
        image_urls=item_creation_image_urls_from_aws,
        options=options,
        item_detail_menu={
            "details": details,
            "fit-sizing": asdict(item_creation_request.fit_sizing),
            "fabric": item_creation_request.fabric,
        },
        description=item_creation_request.description,
        category_codes=item_creation_request.category,
    )

    return item


async def delete_item(item_id: ObjectId) -> int:
    if not (deleted_item := await ItemCollection.delete_by_id(item_id)):
        raise ItemNotFoundException(response_message=f"Item with id {item_id} not found")
    return deleted_item


async def updated_item(item_id: ObjectId,
                       item_update_request: ItemUpdateRequest,
                       item_update_images: Sequence[UploadFile] | None,) -> int:
    if len(data := {key: val for key, val in asdict(item_update_request).items() if val is not None}) > 0:
        if bool(item_update_images):
            item_update_image_urls_from_aws = [
                (await upload_image(image))["url"]
                for image in item_update_images if image.filename != '']
            data["image_urls"] = item_update_image_urls_from_aws
        updated_item_count = await ItemCollection.update_by_id(item_id, data)
        return updated_item_count
    raise NoContentException(response_message="No Contents")


async def get_all_item(page: int) -> list[ItemDocument]:
    offset = (page - 1) * 15
    all_item = await ItemCollection.find_all_item(offset)

    return all_item


async def get_item_by_name(item_name: str) -> list[ItemDocument]:
    filtering_item = await ItemCollection.find_by_name(item_name)

    return filtering_item


async def get_item_by_id(item_id: ObjectId) -> ItemDocument:
    if not (get_one_item := await ItemCollection.find_by_id(item_id)):
        raise NoSuchElementException(response_message="아이템을 찾을 수 없습니다.")

    return get_one_item
