import dataclasses

@dataclasses.dataclass
class UserSigninRequest:
    user_id: str
    password: str