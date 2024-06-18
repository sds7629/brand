from dataclasses import asdict
from typing import Any, cast

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import HttpUrl

from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_document import ShowUserDocument
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
        qna_password: str,
        writer: ShowUserDocument,
        image_url: str | None = None,
        view_count: int = 0,
    ) -> QnADocument:
        result = await cls._collection.insert_one(
            {
                "title": title,
                "payload": payload,
                "image_url": image_url,
                "qna_password": qna_password,
                "writer": asdict(writer),
                "view_count": view_count,
            }
        )

        return QnADocument(
            _id=result.inserted_id,
            title=title,
            payload=payload,
            image_url=image_url,
            qna_password=qna_password,
            writer=writer,
            view_count=view_count,
        )

    @classmethod
    async def find_all_qna(cls) -> list[QnADocument]:
        return [cls._result_dto(result) for result in await cls._collection.find({}).to_list(None)]

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> QnADocument | None:
        result = await cls._collection.find_one({"_id": object_id})
        return cls._result_dto(result) if result else None

    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": object_id})
        return cast(int, result.deleted_count)

    @classmethod
    async def find_by_title(cls, title: str) -> list[QnADocument]:
        return [
            cls._result_dto(result)
            for result in await cls._collection.find({"title": {"$regex": title, "$options": "i"}}).to_list(None)
        ]

    @classmethod
    async def update_by_id(cls, qna_id: ObjectId, data: dict[str, str]) -> int:
        result = await cls._collection.update_one({"_id": qna_id}, {"$set": data}, upsert=False)
        return result.modified_count

    @classmethod
    def _result_dto(cls, result: dict[Any, Any]) -> QnADocument:
        return QnADocument(
            _id=result["_id"],
            title=result["title"],
            payload=result["payload"],
            image_url=result["image_url"],
            qna_password=result["qna_password"],
            writer=result["writer"],
            view_count=result["view_count"],
        )
