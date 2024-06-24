from pydantic import dataclasses


@dataclasses.dataclass
class DuplicatedResponse:
    result: str
