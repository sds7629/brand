from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.config import MAIL_PASSWORD, MAIL_USERNAME

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)

html = """
<p>test email sending</p>
<a href="http://localhost:8080/v1/users/find-password">Find Password</a>
"""


async def find_password_to_email_send(email_data: list[EmailStr]) -> None:
    message = MessageSchema(
        subject="FSO Find Password",
        recipients=email_data,
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
