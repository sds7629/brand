from httpx import AsyncClient

from app.entities.category.category_codes import CategoryCode
from app.main import app


async def test_item_get_name_api() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/items?name=테스트")

        assert response.status_code == 200
        assert [elem["name"] for elem in response.json()["item"]] == ["업데이트 테스트2"]


async def test_all_item_get_api() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/items")

        new_list = [elem for elem in response.json()["item"]]

        assert response.status_code == 200
        assert len(new_list) == 4


async def test_create_item_api() -> None:
    item_creation_request = {
        "name": "api test2",
        "price": 100000,
        "image_url": "https://cdn.imweb.me/thumbnail/20221103/cb05eb08e7fc9.jpg",
        "description": "api test pants",
        "item_quantity": 100,
        "size": "s",
        "category": [CategoryCode.BOTTOM],
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/items/create", json=item_creation_request)

    json_data = response.json()

    assert response.status_code == 201
