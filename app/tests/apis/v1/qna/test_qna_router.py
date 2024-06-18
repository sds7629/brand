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
        response = await client.get("/v1/qna/6671b2a2d6f257bcd9264f1d")

        assert response.status_code == status.HTTP_200_OK


async def test_QnA_삭제하기() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/v1/qna/663cb44edfeda588b0cdf1e3/delete")

        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_QnA_생성하기() -> None:
    header = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQ1ODAyNGZmYjE5ZTRkOTlmOTBmMzQiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNTgzNDg2OX0.cMQJg3AwnPhDtpSlNF5zITXOrNsfujsq69Vs1-wUgyA"
    }
    request_body = {
        "title": "절로가3",
        "payload": "가나다3",
    }
    async with AsyncClient(app=app, base_url="http://test", headers=header) as client:
        response = await client.post("/v1/qna/create", json=request_body)

        assert response.status_code == status.HTTP_201_CREATED
