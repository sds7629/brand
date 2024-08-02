from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional, Sequence

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.notice.notice_document import NoticeDocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db


class NoticeCollection:
    _collection = AsyncIOMotorCollection(db, "notice")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [
                ("title", pymongo.TEXT),
            ]
        )

    @classmethod
    async def insert_one(
        cls,
        title: str,
        payload: str,
        writer: ShowUserDocument,
        updated_at: Optional[datetime] = None,
    ) -> NoticeDocument:
        result = await cls._collection.insert_one(
            {
                "title": title,
                "payload": payload,
                "writer": asdict(writer),
                "updated_at": updated_at,
            }
        )
        return NoticeDocument(
            _id=result.inserted_id,
            title=title,
            payload=payload,
            writer=writer,
            updated_at=updated_at,
        )

    @classmethod
    async def find_by_id(cls, notice_id: ObjectId) -> NoticeDocument | None:
        notice = await cls._collection.find_one({"_id": ObjectId(notice_id)})
        return cls._parse(notice) if notice is not None else None

    @classmethod
    async def find_all_notice(cls, offset: int) -> Sequence[NoticeDocument] | None:
        notice_list = await (
            cls._collection.find({}).sort([("_id", pymongo.DESCENDING)]).limit(15).skip(offset).to_list(None)
        )
        return [cls._parse(notice) for notice in notice_list]

    @classmethod
    async def update_by_id(cls, notice_id: ObjectId, data: dict[str, Any]) -> int:
        result = await cls._collection.update_one(
            {"_id": notice_id},
            {"$set": data},
            upsert=False,
        )
        return result.modified_count

    @classmethod
    async def delete_by_id(cls, notice_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": notice_id})
        return result.deleted_count

    @classmethod
    def _parse(cls, result: dict[Any, Any]) -> NoticeDocument:
        return NoticeDocument(
            _id=result["_id"],
            title=result["title"],
            payload=result["payload"],
            writer=result["writer"],
            updated_at=result["updated_at"],
        )
