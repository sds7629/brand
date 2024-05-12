from bson import ObjectId
from fastapi import status
from httpx import AsyncClient

from app.main import app


async def test_QnA_모두_가져오기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/qna")

        assert response.status_code == status.HTTP_200_OK


async def test_QnA_하나_가져오기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/qna/663cb269b430f78fdb5f006b")

        assert response.status_code == status.HTTP_200_OK


async def test_QnA_삭제하기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/v1/qna/663cb44edfeda588b0cdf1e3/delete")

        assert response.status_code == status.HTTP_204_NO_CONTENT
