import re
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pytz import timezone


class Util:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        return bool(re.match(email_regex, email))

    @classmethod
    async def encode(
        cls,
        data: dict,
        secret_key: str,
        expires_time: str,
        algorithm: str = "HS256",
    ) -> str:
        to_encode = data.copy()
        to_encode.update({"_id": str(data["_id"])})
        expire = datetime.now(timezone("Asia/Seoul")) + timedelta(minutes=float(expires_time))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    @classmethod
    async def decode(cls, token: str, secret_key: str, algorithm: str = "HS256") -> dict | None:
        try:
            return jwt.decode(token, secret_key, algorithms=algorithm)
        except jwt.JWTError:
            return None

    @classmethod
    async def check_token_expire(cls, token: str, secret_key: str, algorithm: str) -> dict | None:
        payload = cls.decode(token, secret_key, algorithm)
        now_time = datetime.timestamp(datetime.now(timezone("Asia/Seoul")))
        if payload and payload["exp"] < now_time:
            return None

        return payload
