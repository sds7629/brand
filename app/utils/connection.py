import os

from motor.motor_asyncio import AsyncIOMotorClient

DB_NAME = os.environ.get("MONGO_DB")

client = AsyncIOMotorClient(DB_NAME)
db = client["FSO"]
# db = client["weeber"]
# import asyncio

# async def print_mongo_version():
#     status = await client.test.command('serverStatus')
#     print(status['version'])
#
# asyncio.run(print_mongo_version())
