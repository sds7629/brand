from pydantic import dataclasses, EmailStr


@dataclasses.dataclass
class UserSetPasswdRequest:
    identity_verification_id: str
    user_email: EmailStr
    new_password: str
    new_password_confirm: str
