from bson import ObjectId
from app.entities.collections.users.user_collection import UserCollection


async def signup_user(user_signup_request):
    user = await UserCollection.insert_one(
        user_signup_request.user_id,
        user_signup_request.email,
        user_signup_request.name,
        user_signup_request.password,
        user_signup_request.gender,
        user_signup_request.nickname,
    )

    return user