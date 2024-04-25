import dataclasses

from app.entities.collections.users.user_collection import  UserCollection


@dataclasses.dataclass
class UserSigninResponse:
    id: str
    access_token: str
    refresh_token: str
    name: str
    nickname: str
