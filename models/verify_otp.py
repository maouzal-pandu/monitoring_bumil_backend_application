from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, Boolean, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class VerifyOtp(Base):
    __tablename__ = "verify_otp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), ForeignKey("user.email"), nullable=False, index=True
    )
    otp: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tujuan: Mapped[str] = mapped_column(
        Enum("registrasi", "reset_password", name="otp_tujuan_enum")
    )
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    reset_token: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    reset_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
