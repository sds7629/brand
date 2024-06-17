from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db


class PaymentCollection:
    _collection = AsyncIOMotorCollection(db, "payment")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("id", pymongo.ASCENDING),
            ]
        )

    @classmethod
    async def find_by_id(cls, payment_id: ObjectId) -> PaymentDocument:
        payment = await cls._collection.find_one({"_id": payment_id})
        return cls._parse(payment) if payment else None

    @classmethod
    async def insert_one(
        cls,
        user: ShowUserDocument,
        order: ObjectId,
        items: Sequence[ItemDocument],
        total_price: int,
        payment_time: datetime,
        is_reviewed: bool = False,
    ) -> PaymentDocument:
        payment = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "order": order,
                "items": [asdict(item) for item in items],
                "total_price": total_price,
                "payment_time": payment_time,
                "is_reviewed": is_reviewed,
            }
        )

        return PaymentDocument(
            _id=payment.inserted_id,
            user=user,
            order=order,
            items=items,
            total_price=total_price,
            payment_time=payment_time + timedelta(hours=9),
        )

    @classmethod
    async def find_by_user_id(cls, user_id: ObjectId) -> Sequence[PaymentDocument]:
        histories = await cls._collection.find({"user._id": user_id}).to_list(None)
        return [cls._parse(history) for history in histories if history is not None]

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> PaymentDocument:
        return PaymentDocument(
            _id=result["_id"],
            user=result["user"],
            order=result["order"],
            items=result["items"],
            total_price=result["total_price"],
            payment_time=result["payment_time"] + timedelta(hours=9),
            is_reviewed=result["is_reviewed"],
        )
