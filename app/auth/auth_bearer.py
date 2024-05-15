import asyncio

from jose import JWTError
from typing import Annotated

from fastapi import Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.utility import Util
from app.config import ACCESS_SECRET_KEY
from app.exceptions import UserNotFoundException, ValidationException
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import UserDocument


oauth2_scheme = OAuth2PasswordBearer("/v1/users/signin")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDocument:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_expire = await Util.check_token_expire(token, ACCESS_SECRET_KEY)
        user = await UserCollection.find_by_user_id(token_expire["payload"]["user_id"])
        if not token_expire["is_expired"]:
            raise ValidationException(response_message="Token is expired")
        if not user:
            raise UserNotFoundException
        return user
    except JWTError:
        raise credentials_exception



