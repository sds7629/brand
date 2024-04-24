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
    _collection = AsyncIOMotorCollection(db, "users")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index([("user_no", pymongo.ASCENDING)], unique=True)

    @classmethod
    async def insert_one(
        cls, user_id: str, email: str, password: str, name: str, gender: str, nickname: str, login_method: str = "page"
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
