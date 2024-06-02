import uuid
from dataclasses import asdict

from datetime import datetime, timedelta
from typing import Any, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.items.item_document import ItemDocument
from app.entities.collections.orders.order_document import OrderDocument
from app.entities.collections.payment.payment_document import PaymentDocument
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
        payment_items: Sequence[PaymentDocument],
        merchant_id: str,
        post_code: str,
        address: str,
        detail_address: str,
        orderer_name: str,
        phone_num: str,
        payment_method: str,
        post_text: str | None = None,
        ordering_date: datetime = datetime.utcnow(),
        is_payment: bool = False,
    ) -> OrderDocument:
        order = await cls._collection.insert_one(
            {
                "user": asdict(user),
                "payment_item": [asdict(item) for item in payment_items],
                "merchant_id": merchant_id,
                "post_code": post_code,
                "address": address,
                "detail_address": detail_address,
                "post_text": post_text,
                "orderer_name": orderer_name,
                "phone_num": phone_num,
                "payment_method": payment_method,
                "ordering_date": ordering_date,
                "is_payment": is_payment,
            }
        )

        return OrderDocument(
            _id=order.inserted_id,
            user=user,
            payment_item=payment_items,
            merchant_id=merchant_id,
            post_code=post_code,
            address=address,
            detail_address=detail_address,
            post_text=post_text,
            orderer_name=orderer_name,
            phone_num=phone_num,
            payment_method=payment_method,
            ordering_date=ordering_date + timedelta(hours=9),
            is_payment=is_payment,
        )

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
            payment_item=result["payment_item"],
            merchant_id=result["merchant_id"],
            post_code=result["post_code"],
            address=result["address"],
            detail_address=result["detail_address"],
            post_text=result["post_text"],
            orderer_name=result["orderer_name"],
            phone_num=result["phone_num"],
            payment_method=result["payment_method"],
            ordering_date=result["ordering_date"] + timedelta(hours=9),
            is_payment=result["is_payment"],
        )
