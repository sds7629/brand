import dataclasses

from app.entities.collections.base_document import BaseDocument


@dataclasses.dataclass
class UserDocument(BaseDocument):
    user_id: str
    email: str
    name: str
    hash_pw: str
    gender: str
    nickname: str
    login_method: str
    is_authenticated: bool = False
    is_delete: bool = False
