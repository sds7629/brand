import dataclasses


@dataclasses.dataclass
class QnARequest:
    title: str
    payload: str
    password: str | None = None
    image_url: str | None = None


@dataclasses.dataclass
class UpdateQnARequest:
    title: str | None
    payload: str | None
    image_url: str | None
