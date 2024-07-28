from pydantic import dataclasses


@dataclasses.dataclass
class NoticeRequest:
    title: str
    payload: str


@dataclasses.dataclass
class UpdateNoticeRequest:
    title: str | None = None
    payload: str | None = None
