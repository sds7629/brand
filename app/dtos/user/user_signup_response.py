import dataclasses



@dataclasses.dataclass
class UserSignupResponse:
    id: str
    name: str
    email: str
    nickname: str
    gender: str