import asyncio
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.qna.qna_collection import QnACollection


async def set_indexes() -> None:
    await asyncio.gather(
        UserCollection.set_index(),
        QnACollection.set_index(),
    )
