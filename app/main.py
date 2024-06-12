from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.apis.cart.v1.cart_router import router as cart_router
from app.apis.item.v1.item_router import router as item_router
from app.apis.oauth_login.v1.kakao_oauth_router import router as kakao_router
from app.apis.order.v1.order_router import router as order_router
from app.apis.payment.v1.payment_router import router as payment_router
from app.apis.qna.v1.qna_router import router as qna_router
from app.apis.user.v1.user_router import router as user_router
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
app.include_router(kakao_router)
app.include_router(order_router)
app.include_router(cart_router)
app.include_router(payment_router)

templates = Jinja2Templates(directory="app/templates")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["home"],
    response_class=HTMLResponse,
)
async def index_home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
