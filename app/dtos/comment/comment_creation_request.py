from pydantic import dataclasses


@dataclasses.dataclass
class CommentCreationRequest:
    payload: str
    base_qna: str
