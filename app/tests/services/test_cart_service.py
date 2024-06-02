from app.entities.collections import UserCollection
from bson import ObjectId
from app.dtos.cart.cart_creation_request import CartCreationRequest, OneCartCreationRequest
from app.services.cart_service import create_cart


async def test_create_cart_service() -> None:
    user_data = await UserCollection.find_by_id(ObjectId("6645800603f02da82f318d98"))
    cart_creation_request = CartCreationRequest(
        items=[
            OneCartCreationRequest(item_id="66583322dc30becfdbf5c51b", quantity=1, color="Black"),
            OneCartCreationRequest(item_id="66583322dc30becfdbf5c51e", quantity=3, color="White"),
        ]
    )

    result = await create_cart(user_data, cart_creation_request)

    assert len(result) == 2
