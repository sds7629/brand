import dataclasses

from pydantic import EmailStr


@dataclasses.dataclass
class UserSignupRequest:
    user_id: str
    email: str
    name: str
    password: str
    nickname: str
    phone_num: str
    is_policy: bool
