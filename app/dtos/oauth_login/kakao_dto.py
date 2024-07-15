from pydantic import dataclasses


@dataclasses.dataclass
class ConfirmIdToken:
    id_token: str


@dataclasses.dataclass
class KakaoAccessToken:
    access_token: str


@dataclasses.dataclass
class KakaoSignResponse:
    access_token: str
    refresh_token: str
