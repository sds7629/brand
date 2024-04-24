import os

from motor.motor_asyncio import AsyncIOMotorClient

DB_NAME = os.environ.get("MONGO_DB", "weeber")

client = AsyncIOMotorClient()
db = client[DB_NAME]

import asyncio

# async def print_mongo_version():
#     status = await client.test.command('serverStatus')
#     print(status['version'])
#
# asyncio.run(print_mongo_version())
