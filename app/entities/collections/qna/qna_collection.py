from dataclasses import asdict
from typing import Any, Sequence, cast

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

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
        writer: ShowUserDocument,
        image_urls: Sequence[str] | None = None,
        is_secret: bool = False,
        is_notice: bool = False,
        view_count: int = 0,
    ) -> QnADocument:
        result = await cls._collection.insert_one(
            {
                "title": title,
                "payload": payload,
                "image_urls": image_urls,
                "writer": asdict(writer),
                "is_secret": is_secret,
                "is_notice": is_notice,
                "view_count": view_count,
            }
        )

        return QnADocument(
            _id=result.inserted_id,
            title=title,
            payload=payload,
            image_urls=image_urls,
            writer=writer,
            is_secret=is_secret,
            is_notice=is_notice,
            view_count=view_count,
        )

    @classmethod
    async def find_all_qna(cls, offset: int) -> list[QnADocument]:
        all_qna = await (
            cls._collection.find({}).sort([("_id", pymongo.DESCENDING)]).limit(15).skip(offset).to_list(length=15)
        )
        return [cls._result_dto(result) for result in all_qna]

    @classmethod
    async def get_all_qna_count(cls) -> int:
        return len(await cls._collection.find({}).to_list(None))

    @classmethod
    async def find_by_id(cls, object_id: ObjectId) -> QnADocument | None:
        result = await cls._collection.find_one({"_id": object_id})
        return cls._result_dto(result) if result else None

    @classmethod
    async def delete_by_id(cls, object_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": object_id})
        return cast(int, result.deleted_count)

    @classmethod
    async def find_by_title(cls, title_keyword: str, offset: int) -> list[QnADocument]:
        return [
            cls._result_dto(result)
            for result in await cls._collection.find({"title": {"$regex": title_keyword, "$options": "i"}})
            .sort([("_id", pymongo.DESCENDING)])
            .limit(15)
            .skip(offset)
            .to_list(None)
        ]

    @classmethod
    async def find_by_payload(cls, payload_keyword: str, offset: int) -> Sequence[QnADocument]:
        return [
            cls._result_dto(result)
            for result in await cls._collection.find({"payload": {"$regex": payload_keyword, "$options": "i"}})
            .sort([("_id", pymongo.DESCENDING)])
            .limit(15)
            .skip(offset)
            .to_list(None)
        ]

    @classmethod
    async def find_by_writer(cls, writer_keyword: str, offset: int) -> Sequence[QnADocument]:
        return [
            cls._result_dto(result)
            for result in await cls._collection.find({"writer": {"$regex": writer_keyword, "$options": "i"}})
            .sort([("_id", pymongo.DESCENDING)])
            .limit(15)
            .skip(offset)
            .to_list(None)
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
            image_urls=result["image_urls"],
            writer=result["writer"],
            is_secret=result["is_secret"],
            is_notice=result["is_notice"],
            view_count=result["view_count"],
        )
