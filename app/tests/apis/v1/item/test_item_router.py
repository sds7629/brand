from httpx import AsyncClient

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
        assert len(new_list) == 3
