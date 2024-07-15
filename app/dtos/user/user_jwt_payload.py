import dataclasses


@dataclasses.dataclass
class UserJWT:
    _id: str
    user_email: str
    nickname: str
