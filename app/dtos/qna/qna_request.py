import dataclasses


@dataclasses.dataclass
class QnARequest:
    title: str
    payload: str
    password: str | None = None
    image_url: str | None = None
