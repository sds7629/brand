from pydantic import dataclasses


@dataclasses.dataclass
class DuplicatedNicknameResponse:
    result: str
