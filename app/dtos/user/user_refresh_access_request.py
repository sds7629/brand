from pydantic import dataclasses

@dataclasses.dataclass
class RefreshAccessRequest:
    user_id: str
    refresh_token: str