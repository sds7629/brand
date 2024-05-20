from datetime import datetime
import pytz

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.items.item_collection import ItemCollection

from bson import ObjectId


async def test_insert_item() -> None:
    name = "멋진 상의"
    price = 20000
    image_url = "https://www.calvinklein.co.kr/dw/image/v2/BGLQ_PRD/on/demandware.static/-/Sites-ck-sea-master-catalog/default/dw6f9397b1/images/CK/KR/C28_01_4MS4K189020_FL-TP-F2.jpg?sw=548&sh=685&q=90"
    description = "겁나게 멋진 옷입니다."
    registration_date = datetime.utcnow()
    item_quantity = 100
    size = "L"
    category = [CategoryCode.TOP]

    result = await ItemCollection.insert_one(
        name = name,
        price = price,
        image_url = image_url,
        description = description,
        registration_date = registration_date,
        item_quantity = item_quantity,
        size = size,
        category = category
    )

    assert result._id is not None
    assert result.name == name
    assert result.item_quantity == item_quantity


async def test_find_by_id() -> None:
    id = "664af218b5f4b3b058c1de33"

    result = await ItemCollection.find_by_id(ObjectId(id))

    assert result.name == "멋진 상의"
    assert result.price == 20000


async def test_delete_by_id() -> None:
    id = "664af218b5f4b3b058c1de33"

    result = await ItemCollection.delete_by_id(ObjectId(id))

    assert type(result) == int
    assert result > 0


async def test_update_by_id() -> None:
    id = "664af218b5f4b3b058c1de33"
    data = {
        "name": "메롱한 상의",
        "updated_at": datetime.utcnow()
    }

    result = await ItemCollection.update_by_id(ObjectId(id), data)

    assert type(result) == int
    assert result > 0


async def test_find_all_item() -> None:
    item = await ItemCollection.find_all_item()

    assert len(item) == 2
    assert type(item) == list


async def test_find_by_name() -> None:
    name = "멋진"

    item = await ItemCollection.find_by_name(name)

    assert len(item) == 1

    ## find 정규식 추가 하는중