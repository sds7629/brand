from httpx import AsyncClient
from fastapi import status
from bson import ObjectId

from app.main import app


async def test_QnA_모두_가져오기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/qna")

        assert response.status_code == status.HTTP_200_OK


async def test_QnA_하나_가져오기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/qna/663b4458c30d6f93286651f4")

        assert response.status_code == status.HTTP_200_OK
