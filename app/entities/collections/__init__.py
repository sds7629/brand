import asyncio

from app.entities.collections.items.item_collection import ItemCollection
from app.entities.collections.qna.qna_collection import QnACollection
from app.entities.collections.users.user_collection import UserCollection


async def set_indexes() -> None:
    await asyncio.gather(
        UserCollection.set_index(),
        QnACollection.set_index(),
        ItemCollection.set_index(),
    )
