from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship

from config.database import Base


class Kehamilan(Base):
    __tablename__ = "kehamilan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    hpht = Column(Date, nullable=False)
    bb_awal = Column(DECIMAL(5, 2), nullable=False)
    gravida = Column(Integer, nullable=False)
    paritas = Column(Integer, nullable=False)
    abortus = Column(Integer, nullable=False)
    status_kehamilan = Column(
        Enum("berlangsung", "selesai", name="kehamilan_enum"),
        default="berlangsung",
        nullable=False,
    )
    status_risiko = Column(
        Enum("rendah", "sedang", "tinggi", name="risiko_enum"),
        default="rendah",
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="kehamilan")
    pemeriksaan = relationship("Pemeriksaan", back_populates="kehamilan")
