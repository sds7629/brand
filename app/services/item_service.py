from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.items.item_collection import ItemCollection
from bson import ObjectId
from dataclasses import asdict
from app.exceptions import NoContentException
async def create_item(item_creation_request: ItemCreationRequest) -> ItemDocument:
    item =  await ItemCollection.insert_one(
        name = item_creation_request.name,
        price = item_creation_request.price,
        image_url = item_creation_request.image_url,
        description = item_creation_request.description,
        registration_date = item_creation_request.registration_date,
        item_quantity = item_creation_request.item_quantity,
        size = item_creation_request.size,
        category=item_creation_request.category,
    )

    return item



async def delete_item(item_id: ObjectId) -> int:
    deleted_item = await ItemCollection.delete_by_id(item_id)
    return deleted_item


async def updated_item(item_id: ObjectId, item_update_request: ItemUpdateRequest) -> int:
    if len(data := {key: val for key, val in asdict(item_update_request).items() if val is not None}) > 1:
        updated_item = await ItemCollection.update_by_id(item_id, data)
        return updated_item
    raise NoContentException(response_message="No Contents")

async def get_all_item() -> list[ItemDocument]:
    all_item = await ItemCollection.find_all_item()

    return all_item

async def get_item_by_id(item_id: ObjectId) -> ItemDocument:
    get_one_item = await ItemCollection.find_by_id(item_id)

    return get_one_item