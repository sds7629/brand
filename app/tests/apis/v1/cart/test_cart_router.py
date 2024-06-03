from httpx import AsyncClient

from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.main import app


async def test_get_cart_api() -> None:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQ1ODAyNGZmYjE5ZTRkOTlmOTBmMzQiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzA3NzU1OH0.qe5e8HqMHE_ohLwNhbeNtQcPnEDPnd8C_9wPas7L-_A",
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(url="v1/cart", headers=headers)

        assert response.status_code == 200


async def test_create_cart_api() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjVkZGZiZTRjMTExNGEzMzNjM2U0OWMiLCJ1c2VyX2lkIjoiYWRtaW4xIiwiZ2VuZGVyIjoibWFsZSIsIm5pY2tuYW1lIjoiYWRtaW4xIiwiZXhwIjoxNzE3NDMwNDM1fQ.B4WBb0DBWfRLuwuATYWZWcGclQGfr53nZ7YPrB3PR_Y"
    }

    cart_creation_request = {
        "items": [
            {"item_id": "665b07704f4f6490716bced6", "quantity": 1, "color": "Black"},
            {"item_id": "665b07704f4f6490716bced7", "quantity": 2, "color": "Black"},
            {"item_id": "665b07704f4f6490716bced8", "quantity": 1, "color": "White"},
            {"item_id": "665b07704f4f6490716bceda", "quantity": 1, "color": "White"},
        ]
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(url="v1/cart/create", headers=headers, json=cart_creation_request)

        assert response.status_code == 201
