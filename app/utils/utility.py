import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

import re
from typing import Any, Union
from app.entities.collections.users.user_collection import pwd_context
from jose import jwt

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
class Util:
    @classmethod
    async def is_valid_email(cls, email:str) -> bool:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(email_regex, email))

    @classmethod
    async def is_valid_password(cls, password:str, input_password: str) -> bool:
        return pwd_context.verify(password, input_password)

    @classmethod
    async def create_access_token(cls, subject:Union[str, Any], expires_delta:float = None) -> str:
        if expires_delta is None:
            from datetime import datetime
            expires_delta += datetime.utcnow()
        else:
            from datetime import datetime,timedelta
            expires_delta += datetime.utcnow() + timedelta(minutes=expires_delta)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt