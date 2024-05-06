import dataclasses


@dataclasses.dataclass
class UserJWT:
    _id: str
    user_id: str
    gender: str
    nickname: str
