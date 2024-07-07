from pydantic import dataclasses


@dataclasses.dataclass
class CommentUpdateRequest:
    payload: str | None = None
