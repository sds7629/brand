from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.orders.order_document import OrderDocument
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
                "item": [asdict(item) for item in items],
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
