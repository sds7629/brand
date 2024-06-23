from pydantic import EmailStr, dataclasses


@dataclasses.dataclass
class EmailSchema:
    email: list[EmailStr]
