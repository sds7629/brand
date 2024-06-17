import os

from redis.asyncio import ConnectionError, Redis

redis: "Redis[str]" = Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True,
    retry_on_error=[ConnectionError],
)
