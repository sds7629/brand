from bson import ObjectId

from app.utils.utility import Util

from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import UserDocument

from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signup_request import UserSignupRequest




ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXFIRES")

async def signup_user(user_signup_request: UserSignupRequest) -> UserDocument:
    if Util.is_valid_email(user_signup_request.email):
        user = await UserCollection.insert_one(
            user_signup_request.user_id,
            user_signup_request.email,
            user_signup_request.name,
            user_signup_request.password,
            user_signup_request.gender,
            user_signup_request.nickname,
        )

        return user

    else:
        raise ValueError('Invalid email')


async def signin_user(user_signin_request:UserSigninRequest) -> UserDocument:
    user = await UserCollection._collection.find_one({"user_id": user_signin_request.user_id})
    if user is None:
        raise ValueError('User not found')
    if Util.is_valid_password(user.hash_pw, user_signin_request.password):
        ...

