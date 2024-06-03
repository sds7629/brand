from httpx import AsyncClient

from app.main import app


async def test_api_get_user_orders() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjVkZGZiZTRjMTExNGEzMzNjM2U0OWMiLCJ1c2VyX2lkIjoiYWRtaW4xIiwiZ2VuZGVyIjoibWFsZSIsIm5pY2tuYW1lIjoiYWRtaW4xIiwiZXhwIjoxNzE3NDMwNDM1fQ.B4WBb0DBWfRLuwuATYWZWcGclQGfr53nZ7YPrB3PR_Y"
    }

    cart_data = {"cart_items": ["665af87eee8ab23dc9c8e621", "665af87eee8ab23dc9c8e622"]}
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        response = await client.get("/v1/orders", headers=headers)

        assert response.status_code == 200


async def test_api_create_order() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjVkZGZiZTRjMTExNGEzMzNjM2U0OWMiLCJ1c2VyX2lkIjoiYWRtaW4xIiwiZ2VuZGVyIjoibWFsZSIsIm5pY2tuYW1lIjoiYWRtaW4xIiwiZXhwIjoxNzE3NDMwNDM1fQ.B4WBb0DBWfRLuwuATYWZWcGclQGfr53nZ7YPrB3PR_Y"
    }

    cart_data = {"cart_id": ["665de6390a3f3c489b5766a0", "665de6390a3f3c489b5766a1"]}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/orders/create", headers=headers, json=cart_data)

        assert response.status_code == 201
