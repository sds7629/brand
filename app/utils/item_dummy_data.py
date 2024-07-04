import asyncio
import os
import random

import certifi
import faker_commerce
import pandas as pd
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import BulkWriteError

from app.entities.category.category_codes import CategoryCode
from app.utils.enums.color_codes import ColorCode
from app.utils.enums.size_codes import SizeCode

ca = certifi.where()
DB_NAME = os.environ.get("MONGO_DB")

client = AsyncIOMotorClient(DB_NAME, tlsCAFile=ca)
db = client["FSO"]

# client = AsyncIOMotorClient()
# db = client["weeber"]

item_collection = AsyncIOMotorCollection(db, "item")

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
data_mount = 100
image_urls_list = [
    "https://wimg.mk.co.kr/news/cms/202302/26/news-p.v1.20230224.233387a1bc574656b1f57f2324ada54e_P1.png",
    "https://i.pinimg.com/736x/4c/e8/b8/4ce8b8eb97d4a948551df946feea3b2a.jpg",
    "https://i.pinimg.com/564x/47/e9/74/47e9742914b497aab11a9e8983db2ad1.jpg",
    "https://i.pinimg.com/564x/94/b7/a8/94b7a8f0e2cd584d43b9229d019c3674.jpg",
    "https://i.pinimg.com/564x/ce/ad/6b/cead6b8c0915d16dd14c6e5979841d95.jpg",
    "https://i.pinimg.com/564x/40/2e/67/402e6772ad229813db3c894ee2ab2a0c.jpg",
    "https://i.pinimg.com/564x/a3/15/e3/a315e3cf628792239eef6cb7d06a4587.jpg",
    "https://i.pinimg.com/564x/40/e9/73/40e973555e53590be908cd7820fa3673.jpg",
]

details = [
    "높은 밀도의 코튼 소재",
    "웨이스트 밴드 드로우 스트링",
    "밑단 스트링 조절 가능",
    "테스트 디테일1",
    "밴드 쩔어서 공연도함",
    "가나다라마바사",
    "오늘 날씨 너무 더움 ㅇㅅㅇ",
    "곧 있으면 장마시작",
]
options = ["black-1", "black-2", "white-1", "white-2"]
model_fit = "165cm 33kg 10 10 10"
item_size = "80 10 29 10"
fabric = "면 100%"

name = [fake.ecommerce_name() for _ in range(data_mount)]
price = [fake.random_int(min=8000, max=20000) for _ in range(data_mount)]
image_urls = [[random.choice(image_urls_list) for _ in range(3)] for _ in range(data_mount)]
options = [{option: 25 for option in options} for _ in range(data_mount)]
item_detail_menu = [
    {
        "details": {f"detail-{_}": random.choice(details) for _ in range(3)},
        "fit_sizing": {
            "model_fit": model_fit,
            "item_size": item_size,
            "fabric": fabric,
        },
    }
    for _ in range(100)
]
description = [fake.paragraph() for _ in range(data_mount)]
registration_date = [fake.date_time_between() for _ in range(data_mount)]
category_codes = [random.choice(category_list) for _ in range(data_mount)]

df = pd.DataFrame()
df["name"] = name
df["price"] = price
df["image_urls"] = image_urls
df["description"] = description
df["registration_date"] = registration_date
df["options"] = options
df["item_detail_menu"] = item_detail_menu
df["category_codes"] = category_codes

records = df.to_dict(orient="records")


async def insert_all() -> None:
    try:
        await client.admin.command("ping")
        print("Connection Done")
    except Exception as e:
        print(e)
    try:
        await item_collection.insert_many(records)
        print(f"inserted {len(records)} records")
    except BulkWriteError:
        print(f"failed to insert {len(records)} records")


asyncio.run(insert_all())
