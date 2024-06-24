from pydantic import dataclasses


@dataclasses.dataclass
class DuplicatedRequest:
    nickname: str | None
    email: str | None
