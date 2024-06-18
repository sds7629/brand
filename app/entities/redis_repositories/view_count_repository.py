from app.utils.redis_ import redis
from app.utils.utility import TimeUtil


class ViewCountRedisRepository:
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

    @classmethod
    async def delete(cls, *key: str) -> None:
        await redis.delete(*key)

    @classmethod
    async def increase_data(cls, key: str) -> None:
        await redis.incr(key)

    @classmethod
    async def add_set(cls, key: str, value: str) -> None:
        if not await redis.exists(key):
            await redis.sadd(key, value),
            await redis.expire(key, (await TimeUtil.to_midnight_seconds())[0])
        else:
            await redis.sadd(key, value)

    @classmethod
    async def is_exist_set(cls, key: str, value: str) -> bool:
        return bool(await redis.sismember(key, value))
