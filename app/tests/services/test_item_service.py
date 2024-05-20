from datetime import datetime

from bson import ObjectId

from app.dtos.item.item_creation_request import ItemCreationRequest
from app.dtos.item.item_update_request import ItemUpdateRequest
from app.entities.category.category_codes import CategoryCode
from app.services.item_service import (
    create_item,
    delete_item,
    get_all_item,
    get_item_by_id,
    updated_item,
)


async def test_아이템_생성() -> None:
    name = "멋진 상의 두 번쨰"
    price = 30000
    image_url = "https://m.thetrillion.co.kr/web/product/medium/202403/6316e7b5eab5478a5dad5bbba9b5a768.jpg"
    description = "겁나게 멋진 옷입니다."
    registration_date = datetime.utcnow()
    item_quantity = 100
    size = "L"
    category = [CategoryCode.TOP]
    creation_request = ItemCreationRequest(
        name=name,
        price=price,
        image_url=image_url,
        description=description,
        registration_date=registration_date,
        item_quantity=item_quantity,
        size=size,
        category=category,
    )
    result = await create_item(creation_request)

    assert result.name == name
    assert result.price == price


async def test_아이템_삭제() -> None:
    id = "664b00109349e9c3adb76924"
    deleted_item = await delete_item(ObjectId(id))

    assert deleted_item is not None
    assert deleted_item > 0


async def test_아이템_수정() -> None:
    id = "664af218b5f4b3b058c1de33"
    update_request = ItemUpdateRequest()
    item = await updated_item(ObjectId(id), update_request)

    assert item is not None
    assert item > 0


async def test_get_item() -> None:
    all_item = await get_all_item()

    assert len(all_item) == 2


async def test_find_item_by_id_service() -> None:
    id = "664af218b5f4b3b058c1de33"

    result = await get_item_by_id(ObjectId(id))

    assert result.price == 20000
    assert result.size == "L"


async def test_find_item_by_name_service() -> None:
    name = "멋진 상의 두 번째"
