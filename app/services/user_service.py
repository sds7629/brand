import asyncio
from typing import Any

from bson import ObjectId

from app.config import (
    ACCESS_SECRET_KEY,
    ACCESS_TOKEN_EXFIRE,
    ALGORITHM,
    REFRESH_SECRET_KEY,
    REFRESH_TOKEN_EXFIRE,
)
from app.dtos.user.user_duplicated_request import DuplicatedRequest
from app.dtos.user.user_refresh_access_request import RefreshAccessRequest
from app.dtos.user.user_signin_request import UserSigninRequest
from app.dtos.user.user_signup_request import UserSignupRequest
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import ShowUserDocument, UserDocument
from app.exceptions import UserNotFoundException, ValidationException
from app.utils.utility import TotalUtil


async def signup_user(user_signup_request: UserSignupRequest) -> UserDocument | None:
    user_validator = await asyncio.gather(
        TotalUtil.is_valid_email(user_signup_request.email),
        TotalUtil.phone_validator(user_signup_request.phone_num),
    )

    if not all(user_validator):
        raise ValidationException(response_message="Invalid email or phone number")

    id_pw_validator = await asyncio.gather(
        TotalUtil.check_special_words(user_signup_request.user_id),
        TotalUtil.check_passwords(user_signup_request.password),
    )

    if not all(id_pw_validator):
        raise ValidationException(response_message="Invalid user ID or password")

    user_id_exist, nickname_exist = await asyncio.gather(
        UserCollection.find_by_user_id(user_signup_request.user_id),
        UserCollection.find_by_nickname(user_signup_request.nickname),
    )

    if user_id_exist or nickname_exist:
        raise ValidationException(response_message="사용할 수 없는 아이디입니다.")

    user = await UserCollection.insert_one(
        user_signup_request.user_id,
        user_signup_request.email,
        user_signup_request.name,
        user_signup_request.password,
        user_signup_request.nickname,
        user_signup_request.phone_num,
    )

    return user


async def signin_user(user_signin_request: UserSigninRequest) -> dict[Any, Any]:
    user = await UserCollection.find_by_user_id(user_signin_request.user_id)

    if not user:
        raise UserNotFoundException(f"가입된 유저가 아닙니다.")

    if user is not None:
        if user.is_delete:
            raise UserNotFoundException(f"가입된 유저가 아닙니다.")

    if await TotalUtil.is_valid_password(user_signin_request.password, user.hash_pw):
        access_token, refresh_token = await asyncio.gather(
            TotalUtil.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE, ALGORITHM),
            TotalUtil.encode(user, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXFIRE, ALGORITHM),
        )
        data = {
            "user_data": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data
    raise UserNotFoundException(response_message="패스워드가 맞지 않습니다.")


async def delete_user(user: ShowUserDocument, user_id: ObjectId) -> None:
    if not (user == await UserCollection.find_by_id(user_id)):
        raise ValueError(f"Permission Denied")
    await UserCollection.delete_by_id(user_id)


async def refresh_access_token(refresh: RefreshAccessRequest) -> dict[str, str]:
    user = await TotalUtil.decode(refresh.refresh_token, REFRESH_SECRET_KEY)
    token_expire = await TotalUtil.check_token_expire(refresh.refresh_token, REFRESH_SECRET_KEY)
    if token_expire["is_expired"]:
        raise ValidationException(response_message="Token is expired")
    access_token = await TotalUtil.encode(user, ACCESS_SECRET_KEY, ACCESS_TOKEN_EXFIRE, ALGORITHM)
    data = {"access_token": access_token}
    return data


async def check_nickname_or_email(nickname_or_email_request: DuplicatedRequest) -> str:
    if not (nickname_or_email_request.nickname or nickname_or_email_request.email):
        raise ValidationException(response_message="한 개 이상의 값을 입력해주세요")
    if nickname_or_email_request.nickname:
        if await UserCollection.find_by_nickname(nickname_or_email_request.nickname):
            return "is_duplicated"
        else:
            return "not_found"

    if nickname_or_email_request.email:
        if await UserCollection.find_by_email(nickname_or_email_request.email):
            return "is_duplicated"
        else:
            return "not_found"
