import asyncio

from app.entities.collections.carts.cart_collection import CartCollection
from app.entities.collections.items.item_collection import ItemCollection
from app.entities.collections.orders.order_collection import OrderCollection
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.comments.comment_collection import CommentCollection


async def set_indexes() -> None:
    await asyncio.gather(
        UserCollection.set_index(),
        QnACollection.set_index(),
        ItemCollection.set_index(),
        OrderCollection.set_index(),
        CartCollection.set_index(),
        CommentCollection.set_index(),
    )
