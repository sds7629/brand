import asyncio
import os
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import BulkWriteError

DB_NAME = os.environ.get("MONGO_DB", "weeber")

client = AsyncIOMotorClient()
db = client[DB_NAME]
item_collection = AsyncIOMotorCollection(db, "item")

from faker import Faker
import faker_commerce
import random

import pandas as pd

from app.entities.category.category_codes import CategoryCode

fake = Faker("ko_KR")
fake.add_provider(faker_commerce.Provider)
Faker.seed(1)

category_list:list[CategoryCode] = [CategoryCode.TOP, CategoryCode.BOTTOM, CategoryCode.OUTER, CategoryCode.CAP, CategoryCode.SHOES]
size_list:list[str] = ["s", "m", "l", "xl", "xls", "xlsx"]
data_mount = 10000



name = [fake.ecommerce_name() for _ in range(data_mount)]
price = [fake.random_int(min = 8000, max = 20000) for _ in range(data_mount)]
image_url = [fake.image_url() for _ in range(data_mount)]
description = [fake.paragraph() for _ in range(data_mount)]
registration_date = [fake.date_time_between() for _ in range(data_mount)]
item_quantity = [100 for _ in range(data_mount)]
size = [random.choice(size_list) for _ in range(data_mount)]
category_codes = [[random.choice(category_list)] for _ in range(data_mount)]


df = pd.DataFrame()
df["name"] = name
df["price"] = price
df["image_url"] = image_url
df["description"] = description
df["registration_date"] = registration_date
df["item_quantity"] = item_quantity
df["size"] = size
df["category_codes"] = category_codes

records = df.to_dict(orient='records')

async def insert_all() -> None:
    try:
        await item_collection.insert_many(records)
    except BulkWriteError:
        print(f"failed to insert {len(records)} records")
    print(f"inserted {len(records)} records")

asyncio.run(insert_all())