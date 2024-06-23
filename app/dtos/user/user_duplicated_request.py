from pydantic import dataclasses


@dataclasses.dataclass
class DuplicatedNicknameRequest:
    nickname: str
