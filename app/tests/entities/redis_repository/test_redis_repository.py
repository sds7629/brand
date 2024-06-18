

async def test_view_count_set_and_get() -> None:
    key = "foo"
    value = "bar"

    from app.entities.redis_repositories.view_count_repository import (
        ViewCountRedisRepository,
    )
    await ViewCountRedisRepository.set(key, value)

    assert await ViewCountRedisRepository.get(key) == value
