from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.users.v1.user_router import router as user_router
from app.entities.collections import set_indexes

app = FastAPI()
app.include_router(user_router)

app.middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await set_indexes()
