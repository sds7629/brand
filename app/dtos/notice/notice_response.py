from datetime import datetime

from pydantic import dataclasses


@dataclasses.dataclass
class NoticeResponse:
    notice_id: str
    title: str
    payload: str
    created_at: datetime
    admin_nickname: str
