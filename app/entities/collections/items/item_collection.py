from typing import Any, cast

from bson import ObjectId

from pydantic import HttpUrl
from motor.motor_asyncio import AsyncIOMotorCollection

from datetime import datetime, timedelta

import pymongo

from app.entities.category.category_codes import CategoryCode
from app.entities.collections.items.item_document import ItemDocument
from app.utils.connection import db


class ItemCollection:
    _collection =  AsyncIOMotorCollection(db, "item")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("item_name", pymongo.TEXT),
                ("category_codes", pymongo.ASCENDING),
            ]
        )


    @classmethod
    async def insert_one(
            cls,
            name: str,
            price: int,
            image_url: HttpUrl,
            description: str,
            registration_date: datetime,
            item_quantity: int,
            size: str,
            category: list[CategoryCode]
            ) -> ItemDocument:
        result = await cls._collection.insert_one(
            {
                "name": name,
                "price": price,
                "image_url": image_url,
                "description": description,
                "registration_date": registration_date,
                "item_quantity": item_quantity,
                "size": size,
                "category": category
            }
        )

        return ItemDocument(
            _id = result.inserted_id,
            name = name,
            price = price,
            image_url = image_url,
            description = description,
            registration_date = registration_date + timedelta(hours=9),
            item_quantity = item_quantity,
            size = size,
            category_codes = category
        )

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> ItemDocument | None:
        result = await cls._collection.find_one({"_id": ObjectId(object_id)})
        return cls._parse(result) if result else None

    @classmethod
    async def find_by_name(cls, name: str) -> ItemDocument | None:
        result = await cls._collection.find_one({"name": name})
        return cls._parse(result) if result else None

    @classmethod
    async def update_by_id(cls, object_id: ObjectId, data: dict[Any, Any]) -> int:
        result = await cls._collection.find_one_and_update({"_id": object_id}, {"$set": data}, upsert= False)
        return result.modified_count
    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": ObjectId(object_id)})
        return cast(int, result.deleted_count)


    @classmethod
    def _parse(cls, result:dict[Any, Any]) -> ItemDocument:
        return ItemDocument(
            _id = result["_id"],
            name = result["name"],
            price = result["price"],
            image_url = result["image_url"],
            description = result["description"],
            registration_date = result["registration_date"] + timedelta(hours=9),
            item_quantity = result["item_quantity"],
            size = result["size"],
            category_codes = result["category"]
        )