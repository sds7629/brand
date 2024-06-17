from typing import Sequence

from app.utils.redis_ import redis


class ViewCountRedisRepository:
    @classmethod
    async def get(cls, key: str) -> int | None:
        cached = await redis.get(key)
        if cached is None:
            return None
        if not cached:
            return
        return len(cached)

    @classmethod
    async def get_list(cls, key) -> Sequence[str]:
        length = await redis.llen(key)
        return await redis.lrange(key, 0, length-1) if length else None

    @classmethod
    async def set(cls, key: str, value: str) -> None:
        await redis.set(key, value)

    @classmethod
    async def set_list(cls, key: str, value: str) -> None:
        await redis.rpush(key, value)

    @classmethod
    async def delete(cls, *key: str) -> None:
        await redis.delete(*key)
