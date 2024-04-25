import dataclasses


@dataclasses.dataclass
class UserSignupRequest:
    user_id:str
    email: str
    name: str
    password:str
    gender: str
    nickname: str

