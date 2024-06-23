from pydantic import dataclasses

from app.config import Config


@dataclasses.dataclass
class Token:
    access_token: str
    refresh_token: str


@dataclasses.dataclass(config=Config)
class UserSigninResponse:
    id: str
    token: list[Token]
    name: str
    nickname: str
