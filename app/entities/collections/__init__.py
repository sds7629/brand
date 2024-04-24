from app.entities.collections.users.user_collection import UserCollection


async def set_indexes() -> None:
    await UserCollection.set_index()
