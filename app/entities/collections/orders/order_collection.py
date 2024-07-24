from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.orders.order_document import OrderDocument, OrderItem
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db
from app.utils.enums.status_codes import StatusCode


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
        order_item: Sequence[OrderItem],
        recipient_name: str,
        merchant_id: str,
        post_code: str,
        address: str,
        detail_address: str,
        requirements: str,
        phone_num: str,
        total_price: int,
        payment_status: StatusCode = StatusCode.ORDER_PLACED,
        is_payment: bool = False,
    ) -> OrderDocument:
        order = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "order_item": [asdict(one_item) for one_item in order_item],
                "recipient_name": recipient_name,
                "merchant_id": merchant_id,
                "post_code": post_code,
                "address": address,
                "detail_address": detail_address,
                "requirements": requirements,
                "phone_num": phone_num,
                "payment_status": payment_status,
                "total_price": total_price,
                "is_payment": is_payment,
            }
        )
        return OrderDocument(
            _id=order.inserted_id,
            user=user,
            order_item=order_item,
            recipient_name=recipient_name,
            merchant_id=merchant_id,
            post_code=post_code,
            address=address,
            detail_address=detail_address,
            requirements=requirements,
            phone_num=phone_num,
            payment_status=payment_status,
            total_price=total_price,
            is_payment=is_payment,
        )

    @classmethod
    async def update_by_order_id(cls, object_id: ObjectId, data: dict[str, Any]) -> int:
        result = await cls._collection.update_one({"_id": object_id}, {"$set": data}, upsert=False)
        return result.matched_count

    @classmethod
    async def update_by_merchant_id(cls, merchant_id: str, data: dict[str, Any]) -> int:
        order = await cls._collection.update_one({"merchant_id": merchant_id}, {"$set": data}, upsert=False)
        return order.modified_count

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> OrderDocument | None:
        order = await cls._collection.find_one({"_id": ObjectId(object_id)})
        return cls._parse(order) if order else None

    @classmethod
    async def find_by_user_id(cls, user_id: ObjectId) -> list[OrderDocument] | None:
        order = await cls._collection.find({"user._id": user_id}).to_list(None)
        return [cls._parse(order_one) for order_one in order if order_one is not None]

    @classmethod
    async def find_by_merchant_id(cls, merchant_id: str) -> OrderDocument | None:
        order = await cls._collection.find_one({"merchant_id": merchant_id})
        return cls._parse(order) if order else None

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> OrderDocument:
        return OrderDocument(
            _id=result["_id"],
            user=result["user"],
            order_item=result["order_item"],
            recipient_name=result["recipient_name"],
            merchant_id=result["merchant_id"],
            post_code=result["post_code"],
            address=result["address"],
            detail_address=result["detail_address"],
            requirements=result["requirements"],
            phone_num=result["phone_num"],
            payment_status=result["payment_status"],
            total_price=result["total_price"],
            is_payment=result["is_payment"],
        )
