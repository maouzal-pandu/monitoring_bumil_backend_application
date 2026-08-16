import enum
from datetime import date, datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class StatusJadwalAnc(str, enum.Enum):
    terjadwal = "terjadwal"
    selesai = "selesai"
    terlewat = "terlewat"
    dibatalkan = "dibatalkan"


class ScheduleAnc(Base):
    __tablename__ = "schedule_anc"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    kehamilan_id: Mapped[int] = mapped_column(ForeignKey("kehamilan.id"))

    tanggal_jadwal: Mapped[date]
    status: Mapped[StatusJadwalAnc] = mapped_column(default=StatusJadwalAnc.terjadwal)

    catatan: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
