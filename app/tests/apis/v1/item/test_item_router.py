from httpx import AsyncClient

from app.entities.category.category_codes import CategoryCode
from app.main import app


async def test_item_get_name_api() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/items?&page=2")
        new_list = [elem for elem in response.json()["item"]]

        assert response.status_code == 200
        assert len(new_list) == 50


async def test_all_item_get_api() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/v1/items")

        new_list = [elem for elem in response.json()["item"]]

        assert response.status_code == 200
        assert len(new_list) == 50


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


async def test_delete_item_api() -> None:
    item_deleted_id = "664af218b5f4b3b058c1de33"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/v1/items/{item_deleted_id}/delete")

    assert response.status_code == 204
