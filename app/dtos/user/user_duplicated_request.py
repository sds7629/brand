from pydantic import dataclasses


@dataclasses.dataclass
class DuplicatedRequest:
    nickname: str | None = None
    email: str | None = None
