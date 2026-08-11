import os

from dotenv import load_dotenv
from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType,
    NameEmail,
)
from pydantic import EmailStr, SecretStr
from typing import cast

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

if MAIL_USERNAME is None or MAIL_PASSWORD is None or MAIL_FROM is None:
    raise ValueError("MAIL_USERNAME, MAIL_PASSWORD atau MAIL_FROM belum di set")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=SecretStr(MAIL_PASSWORD),
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_otp_email(to_email: EmailStr, nama: str, otp_code: str):
    message = MessageSchema(
        subject="Kode Verifikasi Akun",
        recipients=cast(list[NameEmail], [to_email]),
        body=f"Halo {nama},\n\nKode OTP kamu: {otp_code}\nBerlaku 5 menit.",
        subtype=MessageType.plain,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
