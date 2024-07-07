from pydantic import dataclasses

from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class CommentCreationRequest:
    payload: str
    base_qna: str
