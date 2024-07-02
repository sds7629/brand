import asyncio
import math
from typing import Sequence

from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId

from app.entities.collections import QnACollection
from app.entities.collections.items.item_collection import ItemCollection
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.redis_repositories.page_repository import PageRepository
from app.entities.redis_repositories.view_count_repository import (
    ViewCountRedisRepository,
)
from app.utils.redis_ import redis

scheduler = BackgroundScheduler(timezone="Asia/Seoul")


async def save_view_count() -> None:
    view_count_key_list = await ViewCountRedisRepository.get_all()
    qna_id_list: Sequence[str] = [qna_id.replace("view_count_", "") for qna_id in view_count_key_list]
    view_count_list: Sequence[int] = [int(await redis.get(view_count_key)) for view_count_key in view_count_key_list]
    co_list = [
        QnACollection.update_by_id(ObjectId(qna_id), {"view_count": view_count})
        for qna_id, view_count in zip(qna_id_list, view_count_list)
    ]
    await asyncio.gather(*co_list)


async def set_item_page_count() -> None:
    item_page_count = math.ceil(await ItemCollection.get_all_item_mount() / 15)
    if await PageRepository.get("item_page_count") is None:
        await PageRepository.set("item_page_count", "1")
    await PageRepository.set("item_page_count", str(item_page_count))


async def set_qna_page_count() -> None:
    qna_page_count = math.ceil(await QnACollection.get_all_qna_count() / 15)
    if await PageRepository.get("qna_page_count") is None:
        await PageRepository.set("qna_page_count", "1")
    await PageRepository.set("qna_page_count", str(qna_page_count))


def start_scheduler() -> None:
    loop = asyncio.get_event_loop()
    scheduler.add_job(lambda: loop.create_task(save_view_count()), trigger="interval", seconds=180)
    scheduler.add_job(lambda: loop.create_task(set_item_page_count()), trigger="interval", seconds=180)
    scheduler.add_job(lambda: loop.create_task(set_qna_page_count()), trigger="interval", seconds=45)
    scheduler.start()
