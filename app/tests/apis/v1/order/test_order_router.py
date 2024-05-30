from httpx import AsyncClient

from app.main import app


async def test_api_get_user_orders() -> None:
    headers = {
        "Authorization" : f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQ1ODAyNGZmYjE5ZTRkOTlmOTBmMzQiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNjk3MDQ2Mn0.7l5J0dbnTcPSPKZejPnjo1TXTm_lXxqvddJFm0G190Y"
    }
    async with AsyncClient(app = app, base_url= "http://test",) as client:
        response = await client.get("/v1/orders", headers=headers)

        assert response.status_code == 200