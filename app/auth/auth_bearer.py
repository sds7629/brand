import asyncio
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.config import ACCESS_SECRET_KEY
from app.entities.collections.users.user_collection import UserCollection
from app.entities.collections.users.user_document import ShowUserDocument
from app.utils.utility import TotalUtil

oauth2_scheme = OAuth2PasswordBearer("/v1/users/signin")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> ShowUserDocument | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_expire = await TotalUtil.check_token_expire(token, ACCESS_SECRET_KEY)

        if token_expire["is_expired"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Token is expired"},
            )

        user = await UserCollection.find_by_nickname(token_expire["payload"]["nickname"])
        # 이메일로 변경 필요
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"},
            )
        return user
    except JWTError:
        raise credentials_exception


async def get_current_active_user(
    user: Annotated[ShowUserDocument, Depends(get_current_user)]
) -> ShowUserDocument | None:
    if user.is_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"},
        )
    return user


async def get_admin_user(user: Annotated[ShowUserDocument, Depends(get_current_user)]) -> ShowUserDocument | None:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Not enough Permission"},
        )
    return user
