from httpx import AsyncClient

from app.dtos.cart.cart_creation_request import CartCreationRequest
from app.main import app


async def test_get_cart_api() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjYwNjcxYmU1Y2QxZmMyMmM3NDMwOTYiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzY2Mzk0N30.Y9l7SwNu0lYeeiXJrJMkPnLtrkBDK_TncETznmLtGOM"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(url="v1/cart", headers=headers)

        assert response.status_code == 200


async def test_create_cart_api() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjYwNjcxYmU1Y2QxZmMyMmM3NDMwOTYiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzY2Mzk0N30.Y9l7SwNu0lYeeiXJrJMkPnLtrkBDK_TncETznmLtGOM"
    }

    cart_creation_request = {
        "items": [
            {"item_id": "665b07704f4f6490716bced6", "quantity": 101, "color": "Black"},
            {"item_id": "665b07704f4f6490716bced7", "quantity": 2, "color": "Black"},
            {"item_id": "665b07704f4f6490716bced8", "quantity": 1, "color": "White"},
            {"item_id": "665b07704f4f6490716bceda", "quantity": 1, "color": "White"},
        ]
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(url="v1/cart/create", headers=headers, json=cart_creation_request)

        assert response.status_code == 201
