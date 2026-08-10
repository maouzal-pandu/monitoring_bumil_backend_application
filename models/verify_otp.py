from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)

from config.database import Base


class VerifyOtp(Base):
    __tablename__ = "verify_otp"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    otp = Column(String(255), nullable=False, index=True)
    is_used = Column(Boolean, nullable=False, default=False)
    tujuan = Column(Enum("registrasi", "reset_password", name="otp_tujuan_enum"))
    expired_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
