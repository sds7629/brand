import asyncio
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.config import ACCESS_SECRET_KEY
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import ShowUserDocument
from app.exceptions import UserNotFoundException, ValidationException
from app.utils.utility import TotalUtil

oauth2_scheme = OAuth2PasswordBearer("/v1/users/signin")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> ShowUserDocument:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_expire = await TotalUtil.check_token_expire(token, ACCESS_SECRET_KEY)
        if token_expire["is_expired"]:
            raise ValidationException(response_message="Token is expired")
        user = await UserCollection.find_by_nickname(token_expire["payload"]["nickname"])
        # 이메일로 변경 필요
        if not user:
            raise UserNotFoundException
        return user
    except JWTError:
        raise credentials_exception
