from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    nik: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nomer_telepon: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    alamat: Mapped[str] = mapped_column(Text)
    desa_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("desa.id"), nullable=False, index=True
    )
    latitude: Mapped[float] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float] = mapped_column(Numeric(9, 6))
    tanggal_lahir: Mapped[date] = mapped_column(Date, nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("admin", "bidan", "bumil", name="role_enum"), nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    kehamilan = relationship("Kehamilan", back_populates="user")
    pemeriksaan_dilakukan = relationship("Pemeriksaan", back_populates="bidan")
    desa = relationship("Desa", back_populates="user_list")
