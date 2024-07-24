import os

from redis.asyncio import ConnectionError, Redis

redis: "Redis[str]" = Redis.from_url(
    # "redis://localhost:6379/0",
    os.environ.get("REDIS_URL"),
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True,
    retry_on_error=[ConnectionError],
)
