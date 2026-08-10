from sqlalchemy import (
    DECIMAL,
    Column,
    ForeignKey,
    Integer,
    Boolean,
    Enum,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base


class Pemeriksaan(Base):
    __tablename__ = "pemeriksaan"

    id = Column(Integer, primary_key=True)
    bidan_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    kehamilan_id = Column(
        Integer, ForeignKey("kehamilan.id"), nullable=False, index=True
    )

    # T1-T4: BB, TB, TD, TFU
    berat_badan = Column(DECIMAL(5, 2), nullable=False)
    tinggi_badan = Column(DECIMAL(4, 2), nullable=False)
    td_sistolik = Column(Integer, nullable=False)
    td_diastolik = Column(Integer, nullable=False)
    tinggi_fundus = Column(DECIMAL(4, 2), nullable=False)

    # T5: Imunisasi TT
    status_imunisasi_tt = Column(
        Enum("TT1", "TT2", "TT3", "TT4", "TT5", "belum", name="tt_enum"),
        nullable=False,
        default="belum",
    )

    # T6: Tablet Fe
    jumlah_tablet_fe = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Kumulatif tablet Fe yang sudah diberikan",
    )

    # T7: Tes PMS
    hasil_tes_pms = Column(
        Enum("negatif", "positif", "belum_tes", name="pms_enum"),
        nullable=False,
        default="belum_tes",
    )

    # T8: Temu wicara / konseling
    catatan_konseling = Column(Text)

    # T9: Tes Hb
    hb = Column(DECIMAL(4, 2), comment="Kadar hemoglobin (g/dL)")

    # T10: Tes protein urine
    protein_urine = Column(
        Enum(
            "negatif",
            "positif_1",
            "positif_2",
            "positif_3",
            "belum_tes",
            name="protein_urine_enum",
        ),
        nullable=False,
        default="belum_tes",
    )

    # T11: Tes reduksi urine
    reduksi_urine = Column(
        Enum(
            "negatif",
            "positif_1",
            "positif_2",
            "positif_3",
            "belum_tes",
            name="reduksi_urine_enum",
        ),
        nullable=False,
        default="belum_tes",
    )

    # T12: Perawatan payudara + senam hamil
    perawatan_payudara = Column(Boolean, nullable=False, default=False)
    senam_hamil = Column(Boolean, nullable=False, default=False)

    # Kolom tambahan di luar 12T (pemantauan janin), tetap dipertahankan
    lila = Column(DECIMAL(4, 2), nullable=False, comment="Ukur Lingkar Lengan Atas")
    presentasi_janin = Column(
        Enum(
            "kepala",
            "bokong",
            "lintang",
            "belum_masuk_pap",
            name="presentasi_janin_enum",
        )
    )
    denyut_janin = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    kehamilan = relationship("Kehamilan", back_populates="pemeriksaan")
    bidan = relationship("User", back_populates="pemeriksaan_dilakukan")
