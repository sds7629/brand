from datetime import datetime

from pydantic import dataclasses


@dataclasses.dataclass
class CommentResponse:
    base_qna_id: str
    created_at: datetime
    comment_id: str
    writer: str
    payload: str
