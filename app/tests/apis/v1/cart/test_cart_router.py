from httpx import AsyncClient
from app.main import app
from app.dtos.cart.cart_creation_request import CartCreationRequest


async def test_get_cart_api() -> None:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQ1ODAyNGZmYjE5ZTRkOTlmOTBmMzQiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzA3NzU1OH0.qe5e8HqMHE_ohLwNhbeNtQcPnEDPnd8C_9wPas7L-_A",
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(url="v1/cart", headers=headers)

        assert response.status_code == 200


async def test_create_cart_api() -> None:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQ1ODAyNGZmYjE5ZTRkOTlmOTBmMzQiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzA3NzU1OH0.qe5e8HqMHE_ohLwNhbeNtQcPnEDPnd8C_9wPas7L-_A",
    }

    cart_creation_request = {
        "item_id": [
            "66583322dc30becfdbf5c51a",
            "66583322dc30becfdbf5c51b",
            "66583322dc30becfdbf5c51c",
            "66583322dc30becfdbf5c51e",
        ],
        "mount": 4,
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(url="v1/cart/create", headers=headers, json=cart_creation_request)

        assert response.status_code == 201
