from dataclasses import asdict
from typing import Any, Sequence, cast

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.carts.cart_document import CartDocument
from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db


class CartCollection:
    _collection = AsyncIOMotorCollection(db, "cart")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("user._id)", pymongo.ASCENDING),
            ]
        )

    @classmethod
    async def insert_one(
        cls, user: ShowUserDocument, item: ItemDocument, quantity: int, options: str, total_price: int
    ) -> CartDocument:
        result = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "item": asdict(item),
                "options": options,
                "quantity": quantity,
                "total_price": total_price,
            }
        )

        return CartDocument(
            _id=result.inserted_id,
            user=user,
            item=item,
            quantity=quantity,
            options=options,
            total_price=total_price,
        )

    @classmethod
    async def find_user_cart(cls, user_id: ObjectId) -> Sequence[CartDocument]:
        carts = await cls._collection.find({"user._id": user_id}).to_list(None)
        return [cls._parse(cart) for cart in carts if cart is not None]

    @classmethod
    async def find_by_id(cls, cart_id: ObjectId) -> CartDocument:
        cart = await cls._collection.find_one({"_id": cart_id})
        return cls._parse(cart) if cart is not None else None

    @classmethod
    async def delete_by_id(cls, cart_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": cart_id})

        return cast(int, result.deleted_count)

    @classmethod
    async def delete_by_item(cls, item_id: ObjectId, user_id: ObjectId, option: str) -> int:
        result = await cls._collection.delete_one(
            {"item._id": item_id, "user._id": user_id, "options": option},
        )

        return cast(int, result.deleted_count)

    @classmethod
    async def update_by_id(cls, cart_id: ObjectId, data: dict[str, Any]) -> int:
        result = await cls._collection.update_one({"_id": cart_id}, {"$set": data}, upsert=True)
        return result.modified_count

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> CartDocument:
        return CartDocument(
            _id=result["_id"],
            user=result["user"],
            item=result["item"],
            quantity=result["quantity"],
            options=result["options"],
            total_price=result["total_price"],
        )
