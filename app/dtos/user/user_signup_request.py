import dataclasses
from pydantic import EmailStr

@dataclasses.dataclass
class UserSignupRequest:
    user_id: str
    email: str
    name: str
    password: str
    gender: str
    nickname: str
