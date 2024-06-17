from typing import Sequence

from app.utils.redis_ import redis


class ViewCountRepository:
    @classmethod
    async def get(cls, key: str) -> int | None:
        cached = await redis.get(key)
        if cached is None:
            return None
        if not cached:
            return

        return len(cached)

    @classmethod
    async def set(cls, key: str, value: str) -> None:
        await redis.set(key, f"[{value}]")

    @classmethod
    async def delete(cls, *key: str) -> None:
        await redis.delete(*key)
