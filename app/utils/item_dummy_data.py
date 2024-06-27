import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import BulkWriteError

DB_NAME = os.environ.get("MONGO_DB", "weeber")

client = AsyncIOMotorClient()
db = client[DB_NAME]
item_collection = AsyncIOMotorCollection(db, "item")

import random

import faker_commerce
import pandas as pd
from faker import Faker

from app.entities.category.category_codes import CategoryCode
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode

fake = Faker("ko_KR")
fake.add_provider(faker_commerce.Provider)
Faker.seed(1)

category_list: list[CategoryCode] = [
    CategoryCode.TOP,
    CategoryCode.BOTTOM,
    CategoryCode.OUTER,
    CategoryCode.CAP,
    CategoryCode.SHOES,
]

size_list: list[SizeCode] = [
    SizeCode.ONE,
    SizeCode.TWO,
]
color_list: list[ColorCode] = [
    ColorCode.BLACK,
    ColorCode.WHITE,
]
data_mount = 10000
details = [
    "높은 밀도의 코튼 소재",
    "웨이스트 밴드 드로우 스트링",
    "밑단 스트링 조절 가능",
    "테스트 디테일1",
    "밴드 쩔어서 공연도함",
    "가나다라마바사",
    "오늘 날씨 너무 더움','" "곧 있으면 장마시작",
]


name = [fake.ecommerce_name() for _ in range(data_mount)]
price = [fake.random_int(min=8000, max=20000) for _ in range(data_mount)]
image_urls = [[fake.image_url() for _ in range(3)] for _ in range(data_mount)]
description = [fake.paragraph() for _ in range(data_mount)]
registration_date = [fake.date_time_between() for _ in range(data_mount)]
item_quantity = [100 for _ in range(data_mount)]
size = [random.choice(size_list) for _ in range(data_mount)]
color = [random.choice(color_list) for _ in range(data_mount)]
category_codes = [random.choice(category_list) for _ in range(data_mount)]
details = [[random.choice(details) for _ in range(3)] for _ in range(data_mount)]


df = pd.DataFrame()
df["name"] = name
df["price"] = price
df["image_urls"] = image_urls
df["description"] = description
df["registration_date"] = registration_date
df["item_quantity"] = item_quantity
df["size"] = size
df["color"] = color
df["category_codes"] = category_codes
df["details"] = details

records = df.to_dict(orient="records")


async def insert_all() -> None:
    try:
        await item_collection.insert_many(records)
        print(f"inserted {len(records)} records")
    except BulkWriteError:
        print(f"failed to insert {len(records)} records")


asyncio.run(insert_all())
