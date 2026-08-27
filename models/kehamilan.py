from datetime import date, datetime
from decimal import Decimal
import enum

from sqlalchemy import DECIMAL, Date, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class StatusRisiko(enum.Enum):
    rendah = "rendah"
    sedang = "sedang"
    tinggi = "tinggi"


class Kehamilan(Base):
    __tablename__ = "kehamilan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, index=True
    )
    hpht: Mapped[date] = mapped_column(Date, nullable=False)
    bb_awal: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    gravida: Mapped[int] = mapped_column(Integer, nullable=False)
    paritas: Mapped[int] = mapped_column(Integer, nullable=False)
    abortus: Mapped[int] = mapped_column(Integer, nullable=False)
    status_kehamilan: Mapped[str] = mapped_column(
        Enum("berlangsung", "selesai", name="kehamilan_enum"),
        default="berlangsung",
        nullable=False,
    )
    status_risiko: Mapped[str] = mapped_column(
        Enum(StatusRisiko),
        default="rendah",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="kehamilan")
    pemeriksaan = relationship("Pemeriksaan", back_populates="kehamilan")
