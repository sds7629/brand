import dataclasses


@dataclasses.dataclass
class UserJWT:
    _id: str
    email: str
    nickname: str
