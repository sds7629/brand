from pydantic import dataclasses
from app.config import Config


@dataclasses.dataclass(config = Config)
class OrderRequest:
    user_nickname: str