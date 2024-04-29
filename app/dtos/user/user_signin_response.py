import dataclasses


@dataclasses.dataclass
class Token:
    access_token: str
    refresh_token: str


@dataclasses.dataclass
class UserSigninResponse:
    id: str
    token: list[Token]
    name: str
    nickname: str
