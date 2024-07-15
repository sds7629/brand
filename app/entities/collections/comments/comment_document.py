from pydantic import dataclasses

from app.entities.collections.base_document import BaseDocument
from app.entities.collections.qna.qna_document import HttpUrlString, QnADocument
from app.entities.collections.users.user_document import ShowUserDocument


@dataclasses.dataclass
class CommentDocument(BaseDocument):
    writer: ShowUserDocument
    payload: str
    base_qna: QnADocument
