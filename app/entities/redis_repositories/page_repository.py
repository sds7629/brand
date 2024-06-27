from app.utils.redis_ import redis


class PageRepository:

    @classmethod
    async def get(cls, key: str) -> str | None:
        cached = await redis.get(key)
        if cached is None:
            return None
        if not cached:
            return
        return cached

    @classmethod
    async def set(cls, key: str, value: str) -> None:
        await redis.set(key, value)
