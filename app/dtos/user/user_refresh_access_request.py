from pydantic import dataclasses


@dataclasses.dataclass
class RefreshAccessRequest:
    refresh_token: str
