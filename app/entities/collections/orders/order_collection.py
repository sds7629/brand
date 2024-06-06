from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.users.user_document import ShowUserDocument
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
        email: str,
        total_price: int,
        merchant_id: str,
        post_code: str,
        address: str,
        detail_address: str,
        order_name: str,
        phone_num: str,
        payment_method: str,
        requirements: str,
        ordering_item: Sequence[ObjectId],
        ordering_date: datetime = datetime.utcnow(),
        is_payment: bool = False,
    ) -> OrderDocument:
        order = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "merchant_id": merchant_id,
                "email": email,
                "post_code": post_code,
                "address": address,
                "detail_address": detail_address,
                "requirements": requirements,
                "order_name": order_name,
                "phone_num": phone_num,
                "payment_method": payment_method,
                "total_price": total_price,
                "ordering_item": ordering_item,
                "ordering_date": ordering_date,
                "is_payment": is_payment,
            }
        )

        return OrderDocument(
            _id=order.inserted_id,
            user=user,
            email=email,
            merchant_id=merchant_id,
            post_code=post_code,
            address=address,
            detail_address=detail_address,
            requirements=requirements,
            order_name=order_name,
            phone_num=phone_num,
            payment_method=payment_method,
            total_price=total_price,
            ordering_item=ordering_item,
            ordering_date=ordering_date + timedelta(hours=9),
            is_payment=is_payment,
        )

    @classmethod
    async def update_by_order_id(cls, object_id: ObjectId, data: dict[str, Any]) -> int:
        result = await cls._collection.update_one({"_id": object_id}, {"$set": data}, upsert=False)
        return result.matched_count

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> OrderDocument | None:
        order = await cls._collection.find_one({"_id": ObjectId(object_id)})
        return cls._parse(order) if order else None

    @classmethod
    async def find_by_user_id(cls, user_id: ObjectId) -> list[OrderDocument] | None:
        order = await cls._collection.find({"user._id": user_id}).to_list(None)
        return [cls._parse(order_one) for order_one in order if order_one is not None]

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> OrderDocument:
        return OrderDocument(
            _id=result["_id"],
            user=result["user"],
            email=result["email"],
            merchant_id=result["merchant_id"],
            post_code=result["post_code"],
            address=result["address"],
            detail_address=result["detail_address"],
            requirements=result["requirements"],
            order_name=result["order_name"],
            phone_num=result["phone_num"],
            payment_method=result["payment_method"],
            total_price=result["total_price"],
            ordering_item=result["ordering_item"],
            ordering_date=result["ordering_date"] + timedelta(hours=9),
            is_payment=result["is_payment"],
        )
