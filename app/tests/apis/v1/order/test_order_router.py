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


async def test_api_pre_order() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjYwNWI5ZjI1NWRkOTFiNmQ5Y2MwZDMiLCJ1c2VyX2lkIjoiYWRtaW4xIiwiZ2VuZGVyIjoibWFsZSIsIm5pY2tuYW1lIjoiYWRtaW4xIiwiZXhwIjoxNzE3NTk1MzI1fQ.0e8p2lPmPcbXI7N6nPDXVP2fwWoedcackJ5itCZqbgo"
    }

    cart_data = {"cart_id": ["66605ce04467d329b357fc97", "66605ce04467d329b357fc99"]}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/orders/pre-order", headers=headers, json=cart_data)

        assert response.status_code == 201


async def test_api_create_order() -> None:
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjYwNjcxYmU1Y2QxZmMyMmM3NDMwOTYiLCJ1c2VyX2lkIjoiYWRtaW4iLCJnZW5kZXIiOiJtYWxlIiwibmlja25hbWUiOiJhZG1pbiIsImV4cCI6MTcxNzY1ODY4N30.YmNjS2mG0e91e404JWoCwXYnlLTk7LAGgsCPaF2AryI"
    }

    order_data = {
        "email": "wwww22@naver.com",
        "post_code": "01122",
        "address" : "가나다동",
        "detail_address": "지층동",
        "phone_num": "010-9999-1111",
        "order_name": "김아무개",
        "requirements": "문 앞에 놔주세요",
        "payment_method": "Card",
        "total_price": 65858,
        "cart_id": [
            "666155af5c23e1afa2863036",
            "666155af5c23e1afa2863035"
        ]
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/orders/create", headers=headers, json=order_data)

        assert response.status_code == 201