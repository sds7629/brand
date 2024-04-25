from dataclasses import asdict
from typing import Any, cast

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext

from app.entities.collections.users.user_document import UserDocument
from app.utils.connection import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCollection:
    _collection = AsyncIOMotorCollection(db, "user")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [("email", pymongo.TEXT)],
            unique=True,
        )

    @classmethod
    async def insert_one(
        cls, user_id: str, email: str, name: str, password: str, gender: str, nickname: str, login_method: str = "page"
    ) -> UserDocument:
        result = await cls._collection.insert_one(
            {
                "user_id": user_id,
                "email": email,
                "name": name,
                "hash_pw": pwd_context.hash(password),
                "gender": gender,
                "nickname": nickname,
                "login_method": login_method,
            }
        )

        return UserDocument(
            _id=result.inserted_id,
            user_id=user_id,
            name=name,
            hash_pw=pwd_context.hash(password),
            email=email,
            gender=gender,
            nickname=nickname,
            login_method=login_method,
        )

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> UserDocument | None:
        result = await cls._collection.find_one({"_id": object_id})
        return cls._result_dto(result) if result else None

    @classmethod
    async def _result_dto(cls, result: dict[Any, Any]) -> UserDocument:
        return UserDocument(
            _id=result["_id"],
            user_id=result["user_id"],
            email=result["email"],
            name=result["name"],
            hash_pw=result["hash_pw"],
            gender=result["gender"],
            nickname=result["nickname"],
            login_method=result["login_method"],
            is_authenticated=result["is_authenticated"],
            is_delete=result["is_delete"],
        )
