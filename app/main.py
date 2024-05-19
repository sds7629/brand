from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.qna.v1.qna_router import router as qna_router
from app.apis.user.v1.user_router import router as user_router
from app.apis.item.v1.item_router import router as item_router
from app.entities.collections import set_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("시작되었어요!")
    await set_indexes()
    yield
    print("종료되었어요!")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(qna_router)
app.include_router(item_router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
