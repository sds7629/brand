from pydantic import dataclasses


@dataclasses.dataclass
class OrderRequest:
    user_id: str
