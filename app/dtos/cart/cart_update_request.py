from pydantic import dataclasses


@dataclasses.dataclass
class CartUpdateRequest:
    options: str | None = None
    quantity: int | None = None
