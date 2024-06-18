# import pytest_asyncio
#
# from app.utils.connection import db
# from app.utils.redis_ import redis
#
#
# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def setup_db() -> None:
#     for collection_name in await db.list_collection_names():
#         await db.drop_collection(collection_name)
#
#
# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def setup_redis() -> None:
#     await redis.flushall()
