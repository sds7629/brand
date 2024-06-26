from bson import ObjectId

from app.dtos.cart.cart_creation_request import (
    CartCreationRequest,
    OneCartCreationRequest,
)
from app.entities.collections import UserCollection
from app.services.cart_service import create_cart


async def test_create_cart_service() -> None:
    user_data = await UserCollection.find_by_id(ObjectId("6660671be5cd1fc22c743096"))
    cart_creation_request = CartCreationRequest(
        items=[
            OneCartCreationRequest(item_id="665b07704f4f6490716bced6", quantity=1, color="Black"),
            OneCartCreationRequest(item_id="665b07704f4f6490716bced7", quantity=3, color="White"),
        ]
    )

    result = await create_cart(user_data, cart_creation_request)

    assert len(result) == 2
