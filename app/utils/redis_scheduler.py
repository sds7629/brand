import asyncio
from typing import Sequence

from apscheduler.schedulers.background import BackgroundScheduler

from app.entities.collections import QnACollection
from app.entities.redis_repositories.view_count_repository import ViewCountRedisRepository
from app.utils.redis_ import redis
from bson import ObjectId

scheduler = BackgroundScheduler(timezone="Asia/Seoul")


async def save_view_count() -> None:
    view_count_key_list = await ViewCountRedisRepository.get_all()
    qna_id_list: Sequence[str] = [qna_id.replace("view_count_", "") for qna_id in view_count_key_list]
    view_count_list: Sequence[int] = [int(await redis.get(view_count_key)) for view_count_key in
                                      view_count_key_list]
    co_list = [
                QnACollection.update_by_id(ObjectId(qna_id), {"view_count": view_count})
                for qna_id, view_count in zip(qna_id_list, view_count_list)
               ]
    await asyncio.gather(*co_list)


scheduler.add_job(lambda: asyncio.run(save_view_count()), trigger="interval", seconds=180)
