from pydantic import dataclasses


@dataclasses.dataclass
class CommentResponse:
    base_qna_id: str
    total_qna_mount: int
    writer: str
    payload: str
    image_url: str | None
