import dataclasses


@dataclasses.dataclass
class UserSignOutRequest:
    base_user_id: str
