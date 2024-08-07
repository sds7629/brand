from datetime import datetime
from typing import Any

import pytz
from bson import ObjectId

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.items.item_collection import ItemCollection


async def test_insert_item() -> None:
    name = "겁나 멋진 상의"
    price = 30000
    image_urls = [
        "https://www.calvinklein.co.kr/dw/image/v2/BGLQ_PRD/on/demandware.static/-/Sites-ck-sea-master-catalog/default/dw6f9397b1/images/CK/KR/C28_01_4MS4K189020_FL-TP-F2.jpg?sw=548&sh=685&q=90"
    ]
    description = "겁나게 멋진 옷입니다."
    options: dict[str, int] = {
        "black-1": 25,
        "black-2": 25,
        "white-1": 25,
        "white-2": 25,
    }
    item_detail_menu: dict[str, Any] = {
        "details": {
            "detail-1": "낭만 있는 옷입니다.",
            "detail-2": "가나다",
            "detail-3": "라바사",
        },
        "fit-sizing": {"model-fit": "165cm 33kg 90 10 10", "item-size": "80 10 29 10"},
        "fabric": "천을 이용해 만들었어요",
    }
    registration_date = datetime.utcnow()
    category = CategoryCode.TOP

    result = await ItemCollection.insert_one(
        name=name,
        price=price,
        image_urls=image_urls,
        description=description,
        registration_date=registration_date,
        options=options,
        item_detail_menu=item_detail_menu,
        category_codes=category,
    )

    assert result._id is not None
    assert result.name == name


async def test_find_by_id() -> None:
    id = "6684cd495da715845eaa16c3"

    result = await ItemCollection.find_by_id(ObjectId(id))

    assert result.name == "겁나 멋진 상의"
    assert result.price == 30000


async def test_delete_by_id() -> None:
    id = "6684cd495da715845eaa16c3"

    result = await ItemCollection.delete_by_id(ObjectId(id))

    assert type(result) == int
    assert result > 0


async def test_update_by_id() -> None:
    id = "6684cd495da715845eaa16c3"
    data = {"name": "메롱한 상의", "updated_at": datetime.utcnow()}

    result = await ItemCollection.update_by_id(ObjectId(id), data)

    assert type(result) == int
    assert result > 0


async def test_find_all_item() -> None:
    item = await ItemCollection.find_all_item()

    assert len(item) == 1
    assert type(item) == list


async def test_find_by_name() -> None:
    name = "메롱"

    item = await ItemCollection.find_by_name(name)

    assert len(item) == 1
