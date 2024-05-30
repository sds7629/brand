from dataclasses import asdict

from datetime import datetime, timedelta
from typing import Any

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.users.user_document import (
    DeliveryDocument,
    ShowUserDocument,
)
from app.utils.connection import db


class OrderCollection:
    _collection = AsyncIOMotorCollection(db, "order")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [("id", pymongo.ASCENDING), ("user.name", pymongo.TEXT)],
        )

    @classmethod
    async def insert_one(
        cls,
        user: ShowUserDocument,
        ordering_request: str,
        ordering_item: ItemDocument,
        ordering_item_mount: int,
        post_code: str,
        address: DeliveryDocument,
        detail_address: str,
        payment_method: str,
        total_price: int,
        ordering_date: datetime = datetime.utcnow(),
    ) -> OrderDocument:
        order = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "ordering_date": ordering_date,
                "ordering_request": ordering_request,
                "ordering_item": asdict(ordering_item),
                "ordering_item_mount": ordering_item_mount,
                "post_code": post_code,
                "address": asdict(address),
                "detail_address": detail_address,
                "payment_method": payment_method,
                "total_price": total_price,
            }
        )

        return OrderDocument(
            _id=order.inserted_id,
            user=user,
            ordering_date=ordering_date,
            ordering_request=ordering_request,
            ordering_item=ordering_item,
            ordering_item_mount=ordering_item_mount,
            post_code=post_code,
            address=address,
            detail_address=detail_address,
            payment_method=payment_method,
            total_price=total_price,
        )

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> OrderDocument | None:
        order = await cls._collection.find_one({"_id": ObjectId(object_id)})
        return cls._parse(order) if order else None

    @classmethod
    async def find_by_user_nickname(cls, user_nickname: str) -> list[OrderDocument] | None:
        order = await cls._collection.find({"user.nickname": user_nickname}).to_list(None)
        return [cls._parse(order_one) for order_one in order if order_one is not None]

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> OrderDocument:
        return OrderDocument(
            _id=result["_id"],
            user=result["user"],
            ordering_date=result["ordering_date"] + timedelta(hours=9),
            ordering_request=result["ordering_request"],
            ordering_item=result["ordering_item"],
            ordering_item_mount=result["ordering_item_mount"],
            post_code=result["post_code"],
            address=result["address"],
            detail_address=result["detail_address"],
            payment_method=result["payment_method"],
            total_price=result["total_price"],
        )
