import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

from bson import ObjectId

from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signup_request import UserSignupRequest
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import UserDocument
from app.exceptions import ValidationException
from app.utils.utility import Util

ACCESS_TOKEN_EXFIRE = os.environ.get("ACCESS_TOKEN_EXFIRES")
REFRESH_TOKEN_EXFIRE = os.environ.get("REFRESH_TOKEN_EXFIRES")
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


async def signup_user(user_signup_request: UserSignupRequest) -> UserDocument:
    if await Util.is_valid_email(user_signup_request.email) and await Util.phone_validator(
        user_signup_request.phone_num
    ):
        user = await UserCollection.insert_one(
            user_signup_request.user_id,
            user_signup_request.email,
            user_signup_request.name,
            user_signup_request.password,
            user_signup_request.gender,
            user_signup_request.nickname,
            user_signup_request.phone_num,
        )

        return user
    else:

        raise ValidationException(
            f"유저의 {user_signup_request.email} 혹은 {user_signup_request.phone_num}이 잘못 되었습니다."
        )


async def signin_user(user_signin_request: UserSigninRequest) -> dict:
    user = await UserCollection._collection.find_one({"user_id": user_signin_request.user_id})
    if user["is_delete"]:
        raise ValueError("Deleted User!")

    if await Util.is_valid_password(user_signin_request.password, user["hash_pw"]):
        access_token = await Util.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE, ALGORITHM)
        refresh_token = await Util.encode(user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE, ALGORITHM)
        data = {
            "user_data": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data
    return None


async def delete_user(user_id: ObjectId) -> None:
    if not (shop := await UserCollection.find_by_id(user_id)):
        raise ValueError(f"{user_id}User not found")
    await UserCollection.delete_by_id(user_id)
