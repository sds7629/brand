from dataclasses import asdict

from bson import ObjectId

from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.collections.items.item_collection import ItemCollection
from app.entities.collections.items.item_document import ItemDocument
from app.exceptions import NoContentException, ItemNotFoundException


async def create_item(item_creation_request: ItemCreationRequest) -> ItemDocument:
    item = await ItemCollection.insert_one(
        name=item_creation_request.name,
        price=item_creation_request.price,
        image_url=item_creation_request.image_url,
        description=item_creation_request.description,
        item_quantity=item_creation_request.item_quantity,
        size=item_creation_request.size,
        category=item_creation_request.category,
    )

    return item


async def delete_item(item_id: ObjectId) -> int:
    if not(deleted_item := await ItemCollection.delete_by_id(item_id)):
        raise ItemNotFoundException(response_message=f"Item with id {item_id} not found")
    return deleted_item


async def updated_item(item_id: ObjectId, item_update_request: ItemUpdateRequest) -> int:
    if len(data := {key: val for key, val in asdict(item_update_request).items() if val is not None}) > 1:
        updated_item = await ItemCollection.update_by_id(item_id, data)
        return updated_item
    raise NoContentException(response_message="No Contents")


async def get_all_item(page: int | None = None) -> list[ItemDocument]:
    offset = (page - 1) * 50
    all_item = await ItemCollection.find_all_item(offset)

    return all_item


async def get_item_by_name(item_name: str) -> list[ItemDocument]:
    filtering_item = await ItemCollection.find_by_name(item_name)

    return filtering_item


async def get_item_by_id(item_id: ObjectId) -> ItemDocument:
    get_one_item = await ItemCollection.find_by_id(item_id)

    return get_one_item
