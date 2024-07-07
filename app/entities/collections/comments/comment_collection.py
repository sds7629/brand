from typing import Any, Sequence

import pymongo

from motor.motor_asyncio import AsyncIOMotorCollection

from app.entities.collections.comments.comment_document import CommentDocument
from app.entities.collections.qna.qna_document import QnADocument
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.connection import db

from dataclasses import asdict
from bson import ObjectId


class CommentCollection:
    _collection = AsyncIOMotorCollection(db, "comment")

    @classmethod
    async def set_index(cls) -> None:
        await cls._collection.create_index(
            [("base_qna", pymongo.DESCENDING)],
        )

    @classmethod
    async def insert_one(
            cls,
            writer: ShowUserDocument,
            payload: str,
            base_qna: QnADocument,
            image_url: str = None,
    ) -> CommentDocument:
        result = await cls._collection.insert_one(
            {
                "writer": asdict(writer),
                "payload": payload,
                "base_qna": asdict(base_qna),
                "image_url": image_url,
            }
        )
        return CommentDocument(
            _id=result.inserted_id,
            writer=writer,
            payload=payload,
            base_qna=base_qna,
            image_url=image_url,
        )

    @classmethod
    async def find_by_id(cls, comment_id: ObjectId) -> CommentDocument:
        result = await cls._collection.find_one({"_id": comment_id})
        return cls._parse(result) if result else None

    @classmethod
    async def find_by_base_qna(cls, base_qna: ObjectId) -> Sequence[CommentDocument]:
        result = await cls._collection.find({"base_qna._id": base_qna}).sort([("_id", pymongo.DESCENDING)]).to_list(None)
        return [cls._parse(comment) for comment in result if comment is not None]

    @classmethod
    async def get_all_comment_from_qna(cls, qna_id: ObjectId) -> int:
        result = await cls._collection.find({"base_qna._id": qna_id}).to_list(None)
        return len(result)

    @classmethod
    async def update_by_id(cls, comment_id: ObjectId, data: dict[str, Any]) -> int:
        result = await cls._collection.update_one({"_id": comment_id}, {"$set": data}, upsert=False)
        return result.modified_count

    @classmethod
    async def delete_by_id(cls, comment_id: ObjectId) -> int:
        result = await cls._collection.delete_one({"_id": comment_id})
        return result.deleted_count

    @classmethod
    def _parse(cls, result: dict[str, Any]) -> CommentDocument:
        return CommentDocument(
            _id=result["_id"],
            writer=result["writer"],
            payload=result["payload"],
            base_qna=result["base_qna"],
            image_url=result["image_url"],
        )