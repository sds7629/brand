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
        response = await client.get("/v1/items?page=1")

        new_list = [elem for elem in response.json()["item"]]

        assert response.status_code == 200
        assert len(new_list) == 15


async def test_create_item_api() -> None:
    item_creation_request = {
        "name": "api test2",
        "price": 100000,
        "description": "api test pants",
        "item_quantity": 100,
        "size": "1",
        "color": "black",
        "category": "bottom",
        "details": [
            "높은 밀도의 코튼 소재",
            "웨이스트 밴드 드로우 스트링",
            "밑단 스트링 조절 가능",
        ],
    }
    image_path = "screenshot.png"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/items/create", data=item_creation_request, files={"image": image_path})

    json_data = response.json()

    assert response.status_code == 201


async def test_delete_item_api() -> None:
    item_deleted_id = "664af218b5f4b3b058c1de33"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/v1/items/{item_deleted_id}/delete")

    assert response.status_code == 204


async def test_한개_데이터_가져오기() -> None:
    item_id = "667ba0968328374933ae6d30"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/v1/items/{item_id}")

        assert response.status_code == 200
