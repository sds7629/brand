from app.entities.collections import UserCollection, ItemCollection
from app.entities.collections.carts.cart_collection import CartCollection

from bson import ObjectId
async def test_cart_insert_one() -> None:
    user = await UserCollection.find_by_nickname(nickname="admin")
    items = await ItemCollection.find_all_item(offset = 0)
    mount = len(items[:3])
    price = sum([item.price for item in items[:3]])
    result = await CartCollection.insert_one(
        user = user,
        items = items[:3],
        mount = mount,
        total_price = price,
    )

    assert result.user == user
    assert result.total_price == price



async def test_find_user_cart() -> None:
    carts = await CartCollection.find_user_cart(user_id=ObjectId("66458024ffb19e4d99f90f34"))

    assert len(carts) == 2
    assert carts[0].items[0].price == 17858


async def test_delete_user_cart() -> None:
    deleted_cart = await CartCollection.delete_by_id(ObjectId("6658292513ce1abc2238dd3a"))

    assert deleted_cart == 1