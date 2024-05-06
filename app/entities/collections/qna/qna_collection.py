from dataclasses import asdict
from bson import ObjectId
from typing import Any, cast

import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_document import UserDocument, ShowUserDocument
from app.utils.connection import db


class QnACollection:
    _collection = AsyncIOMotorCollection(db, "qna")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [("title", pymongo.TEXT)],
        )

    @classmethod
    async def insert_one(
        cls,
        title: str,
        payload: str,
        image_url: str | None,
        qna_password: str,
        writer: list[ShowUserDocument],
    ) -> QnADocument:
        result = await cls._collection.insert_one(
            {
                "title": title,
                "payload": payload,
                "image_url": image_url,
                "qna_password": qna_password,
                "writer": [asdict(user) for user in writer],
            }
        )

        return QnADocument(
            _id=result.inserted_id,
            title=title,
            payload=payload,
            image_url=image_url,
            qna_password=qna_password,
            writer=writer,
        )

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> QnADocument | None:
        result = await cls._collection.find_one({"_id": ObjectId(object_id)})
        return cls._result_dto(result) if result else None

    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": ObjectId(object_id)})
        return cast(int, result.deleted_count)

    @classmethod
    async def find_by_title(cls, title: str) -> QnADocument | None:
        result = await cls._collection.find_one({"title": title})
        return cls._result_dto(result) if result else None

    @classmethod
    def _result_dto(cls, result: dict[Any, Any]) -> QnADocument:
        return QnADocument(
            _id=result["_id"],
            title=result["title"],
            payload=result["payload"],
            image_url=result["image_url"],
            qna_password=result["qna_password"],
            writer=result["writer"],
        )
