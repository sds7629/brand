from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.payment.payment_document import PaymentDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db
from app.utils.enums.payment_codes import PaymentMethodCode


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
    async def find_by_merchant_id(cls, merchant_id: str) -> PaymentDocument:
        payment = await cls._collection.find_one({"merchant_id": merchant_id})
        return cls._parse(payment) if payment else None

    @classmethod
    async def insert_one(
        cls,
        user: ShowUserDocument,
        payment_name: str,
        total_price: int,
        merchant_id: str,
        payment_time: datetime,
        payment_method: PaymentMethodCode | None = None,
        payment_status: bool = False,
        fail_reason: str = None,
    ) -> PaymentDocument:
        payment = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "merchant_id": merchant_id,
                "payment_name": payment_name,
                "total_price": total_price,
                "payment_time": payment_time,
                "payment_method": payment_method,
                "payment_status": payment_status,
                "fail_reason": fail_reason,
            }
        )

        return PaymentDocument(
            _id=payment.inserted_id,
            user=user,
            merchant_id=merchant_id,
            payment_name=payment_name,
            total_price=total_price,
            payment_time=payment_time + timedelta(hours=9),
            payment_method=payment_method,
            payment_status=payment_status,
            fail_reason=fail_reason,
        )

    @classmethod
    async def find_by_user_id(cls, user_id: ObjectId) -> Sequence[PaymentDocument]:
        histories = await cls._collection.find({"user._id": user_id}).to_list(None)
        return [cls._parse(history) for history in histories if history is not None]

    @classmethod
    async def update_by_id(cls, payment_id: ObjectId, data: dict[str, Any]) -> int:
        updated_payment = await cls._collection.update_one(
            {"_id": payment_id}, {"$set": data}, upsert=False,
        )
        return updated_payment.modified_count

    @classmethod
    async def update_by_merchant_id(cls, merchant_id: str, data: dict[str, Any]) -> int:
        updated_payment = await cls._collection.update_one(
            {"merchant_id": merchant_id}, {"$set": data}, upsert=False,
        )

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> PaymentDocument:
        return PaymentDocument(
            _id=result["_id"],
            user=result["user"],
            merchant_id=result["merchant_id"],
            payment_name=result["payment_name"],
            total_price=result["total_price"],
            payment_time=result["payment_time"] + timedelta(hours=9),
            payment_method=result["payment_method"],
            payment_status=result["payment_status"],
            fail_reason=result["fail_reason"],
        )
