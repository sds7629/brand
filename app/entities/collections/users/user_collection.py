from dataclasses import asdict
from typing import Any

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.users.user_document import (
    DeliveryDocument,
    ShowUserDocument,
    UserDocument,
)
from app.utils.connection import db
from app.utils.utility import TotalUtil


class UserCollection:
    _collection = AsyncIOMotorCollection(db, "user")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("user_id", pymongo.TEXT),
                ("nickname", pymongo.TEXT),
            ],
            unique=True,
        )

    @classmethod
    async def insert_one(
        cls,
        user_id: str,
        email: str,
        name: str,
        password: str,
        nickname: str,
        phone_num: str,
        login_method: str = "page",
        is_authenticated: bool = False,
        is_delete: bool = False,
        is_admin: bool = False,
        delivery_area: list[DeliveryDocument] = [],
    ) -> UserDocument:
        result = await cls._collection.insert_one(
            {
                "user_id": user_id,
                "email": email,
                "name": name,
                "hash_pw": await TotalUtil.get_hashed_password(password),
                "nickname": nickname,
                "phone_num": phone_num,
                "login_method": login_method,
                "is_authenticated": is_authenticated,
                "is_delete": is_delete,
                "is_admin": is_admin,
                "delivery_area": [asdict(area) for area in delivery_area],
            }
        )

        return UserDocument(
            _id=result.inserted_id,
            user_id=user_id,
            name=name,
            hash_pw=await TotalUtil.get_hashed_password(password),
            email=email,
            nickname=nickname,
            login_method=login_method,
            phone_num=phone_num,
            is_authenticated=is_authenticated,
            is_delete=is_delete,
            is_admin=is_admin,
            delivery_area=delivery_area,
        )

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> ShowUserDocument | None:
        result = await cls._collection.find_one({"_id": object_id})
        return cls._result_show_user_document_dto(result) if result else None

    @classmethod
    async def find_by_user_id(cls, user_id: str) -> UserDocument | None:
        result = await cls._collection.find_one({"user_id": user_id})
        return cls._result_base_user_document_dto(result) if result else None

    @classmethod
    async def find_by_nickname(cls, nickname: str) -> ShowUserDocument | None:
        result = await cls._collection.find_one({"nickname": nickname})
        return cls._result_show_user_document_dto(result) if result else None

    @classmethod
    async def find_by_email(cls, email: str) -> ShowUserDocument | None:
        result = await cls._collection.find_one({"email": email})
        return cls._result_show_user_document_dto(result) if result else None

    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> ShowUserDocument | None:
        result = await cls._collection.update_one(
            {"_id": object_id},
            {"$set": {"is_delete": True}},
        )
        return cls._result_show_user_document_dto(result) if result else None

    @classmethod
    def _result_show_user_document_dto(cls, result: dict[Any, Any]) -> ShowUserDocument:
        return ShowUserDocument(
            _id=result["_id"],
            user_id=result["user_id"],
            email=result["email"],
            name=result["name"],
            nickname=result["nickname"],
            is_delete=result["is_delete"],
            is_admin=result["is_admin"],
            delivery_area=result["delivery_area"],
        )

    @classmethod
    def _result_base_user_document_dto(cls, result: dict[Any, Any]) -> UserDocument:
        return UserDocument(
            _id=result["_id"],
            user_id=result["user_id"],
            email=result["email"],
            name=result["name"],
            hash_pw=result["hash_pw"],
            nickname=result["nickname"],
            phone_num=result["phone_num"],
            login_method=result["login_method"],
            is_authenticated=result["is_authenticated"],
            is_delete=result["is_delete"],
            is_admin=result["is_admin"],
            delivery_area=result["delivery_area"],
        )
