from datetime import datetime, timedelta
from typing import Any, Sequence, cast

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import HttpUrl

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.items.item_document import ItemDocument
from app.utils.connection import db
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode


class ItemCollection:
    _collection = AsyncIOMotorCollection(db, "item")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("name", pymongo.TEXT),
                ("category_codes", pymongo.TEXT),
            ]
        )

    @classmethod
    async def insert_one(
        cls,
        name: str,
        color: ColorCode,
        price: int,
        image_urls: Sequence[HttpUrl],
        description: str,
        item_quantity: int,
        size: SizeCode,
        category_codes: CategoryCode,
        details: Sequence[str],
        registration_date: datetime = datetime.utcnow(),
    ) -> ItemDocument:
        result = await cls._collection.insert_one(
            {
                "name": name,
                "color": color,
                "price": price,
                "image_url": [str(image_url) for image_url in image_urls],
                "description": description,
                "registration_date": registration_date,
                "item_quantity": item_quantity,
                "size": size,
                "category_codes": category_codes,
                "details": details,
            }
        )

        return ItemDocument(
            _id=result.inserted_id,
            name=name,
            color=color,
            price=price,
            image_urls=image_urls,
            description=description,
            registration_date=registration_date + timedelta(hours=9),
            item_quantity=item_quantity,
            size=size,
            category_codes=category_codes,
            details=details,
        )

    @classmethod
    async def find_all_item(cls, offset: int) -> list[ItemDocument] | None:
        all_item = await cls._collection.find({}).limit(15).skip(offset).to_list(length=15)
        return [cls._parse(item) for item in all_item if item is not None]

    @classmethod
    async def get_all_item_mount(cls) -> int:
        return len(await cls._collection.find({}).to_list(None))

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> ItemDocument | None:
        result = await cls._collection.find_one({"_id": object_id})
        return cls._parse(result) if result else None

    @classmethod
    async def find_by_name(cls, name: str) -> list[ItemDocument] | None:
        filtering_item = await cls._collection.find({"name": {"$regex": name, "$options": "i"}}).to_list(length=15)
        return [cls._parse(item) for item in filtering_item if item is not None]

    @classmethod
    async def update_by_id(cls, object_id: ObjectId, data: dict[Any, Any]) -> int:
        result = await cls._collection.update_one({"_id": object_id}, {"$set": data}, upsert=False)
        return result.modified_count

    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": object_id})
        return cast(int, result.deleted_count)

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> ItemDocument:
        return ItemDocument(
            _id=result["_id"],
            name=result["name"],
            color=result["color"],
            price=result["price"],
            image_urls=result["image_urls"],
            description=result["description"],
            registration_date=result["registration_date"] + timedelta(hours=9),
            item_quantity=result["item_quantity"],
            size=result["size"],
            category_codes=result["category_codes"],
            details=result["details"],
        )

    @property
    def collection(self):
        return self._collection
