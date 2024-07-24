from pydantic import dataclasses


@dataclasses.dataclass
class NaverCode:
    code: str
    state: str


@dataclasses.dataclass
class NaverSignResponse:
    access_token: str
    refresh_token: str