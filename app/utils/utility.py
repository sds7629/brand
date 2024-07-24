import re
from dataclasses import asdict
from datetime import datetime, time, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from pytz import timezone

from app.config import ACCESS_TOKEN_EXFIRE
from app.dtos.user.user_jwt_payload import UserJWT
from app.entities.collections.users.user_document import UserDocument


class TotalUtil:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _algorithm = "HS256"

    @classmethod
    async def get_hashed_password(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @classmethod
    async def is_valid_password(cls, input_password: str, save_password: str) -> bool:
        return cls._pwd_context.verify(input_password, save_password)

    @classmethod
    async def phone_validator(cls, phone_number: str) -> bool:
        phone_regex = r"\d{2,3}-\d{3,4}-\d{4}$"
        return bool(re.match(phone_regex, phone_number))

    @classmethod
    async def is_valid_email(cls, email: str) -> bool:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.fullmatch(email_regex, email))

    @classmethod
    async def encode(
        cls,
        data: dict[Any, Any] | UserDocument,
        secret_key: str,
        expires_time: str,
        algorithm: str = "HS256",
    ) -> str:
        if type(data) is UserDocument:
            to_encode = asdict(
                UserJWT(
                    _id=str(data.id),
                    email=data.email,
                    nickname=data.nickname if data.nickname is not None else data.name,
                )
            )
        else:
            to_encode = asdict(
                UserJWT(
                    _id=str(data["_id"]),
                    email=data["email"],
                    nickname=data["nickname"] if data["nickname"] is not None else data["name"],
                )
            )
        expire = datetime.now(timezone("Asia/Seoul")) + timedelta(minutes=float(expires_time))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    @classmethod
    async def decode(cls, token: str, secret_key: str) -> dict[Any, Any] | None:
        try:
            return jwt.decode(token, secret_key, algorithms=cls._algorithm)
        except jwt.JWTError:
            return None

    @classmethod
    async def check_token_expire(
        cls,
        token: str,
        secret_key: str,
    ) -> dict[Any, Any] | None:
        payload = await cls.decode(token, secret_key)
        now_time = datetime.timestamp(datetime.now(timezone("Asia/Seoul")))
        if payload and payload["exp"] > now_time:
            return {
                "payload": payload,
                "is_expired": False,
            }
        else:
            return {"is_expired": True}

    @classmethod
    async def new_access_token(cls, token: str, secret_key: str) -> str | None:
        payload = await cls.decode(token, secret_key)
        now_time = datetime.timestamp(datetime.now(timezone("Asia/Seoul")))
        if payload and payload["exp"] > now_time:
            return None
        return await cls.encode(
            payload,
            secret_key,
            ACCESS_TOKEN_EXFIRE,
        )

    @classmethod
    async def check_special_words(cls, check_str: str) -> bool:
        special_words = "[${}()\[\]]"
        return not bool(re.search(special_words, check_str))

    @classmethod
    async def check_passwords(cls, check_passwd: str) -> bool:
        passwd_regex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        return bool(re.fullmatch(passwd_regex, check_passwd))


class TimeUtil:
    @classmethod
    async def to_midnight_seconds(cls) -> tuple[timezone, ...]:

        now = datetime.utcnow() + timedelta(hours=9)

        if now.time() > time(0, 0):
            next_midnight = datetime.combine(now.date() + timedelta(days=1), time(0, 0))
        else:
            next_midnight = datetime.combine(now.date(), time(0, 0))

        seconds_to_midnight = next_midnight - now

        return seconds_to_midnight, next_midnight

    @classmethod
    async def get_created_at_from_id(cls, object_id: str) -> datetime:
        to_time = object_id[:8]
        time_to_ten = int(to_time, 16)
        timestamp_created_at = datetime.fromtimestamp(time_to_ten) + timedelta(hours=9)
        return timestamp_created_at
