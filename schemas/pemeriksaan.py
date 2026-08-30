from pydantic import BaseModel
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

TTStatus = Literal["TT1", "TT2", "TT3", "TT4", "TT5", "belum"]
PMSResult = Literal["negatif", "positif", "belum_tes"]
UrineResult = Literal["negatif", "positif_1", "positif_2", "positif_3", "belum_tes"]
PresentasiJanin = Literal["kepala", "bokong", "lintang", "belum_masuk_pap"]


class InsertAntenatalCare(BaseModel):
    bidan_id: int
    kehamilan_id: int

    berat_badan: Decimal
    tinggi_badan: Decimal
    td_sistolik: int
    td_diastolik: int
    tinggi_fundus: Decimal

    status_imunisasi_tt: TTStatus = "belum"
    jumlah_tablet_fe: int = 0
    hasil_tes_pms: PMSResult = "belum_tes"
    catatan_konseling: Optional[str] = None
    hb: Optional[Decimal] = None
    protein_urine: UrineResult = "belum_tes"
    reduksi_urine: UrineResult = "belum_tes"
    perawatan_payudara: bool = False
    senam_hamil: bool = False

    lila: Decimal
    presentasi_janin: Optional[PresentasiJanin] = None
    denyut_janin: int


class UpdateAntenatalCare(BaseModel):
    berat_badan: Optional[Decimal] = None
    tinggi_badan: Optional[Decimal] = None
    td_sistolik: Optional[int] = None
    td_diastolik: Optional[int] = None
    tinggi_fundus: Optional[Decimal] = None

    status_imunisasi_tt: Optional[TTStatus] = None
    jumlah_tablet_fe: Optional[int] = None
    hasil_tes_pms: Optional[PMSResult] = None
    catatan_konseling: Optional[str] = None
    hb: Optional[Decimal] = None
    protein_urine: Optional[UrineResult] = None
    reduksi_urine: Optional[UrineResult] = None
    perawatan_payudara: Optional[bool] = None
    senam_hamil: Optional[bool] = None

    lila: Optional[Decimal] = None
    presentasi_janin: Optional[PresentasiJanin] = None
    denyut_janin: Optional[int] = None


class ResponseAntenatalCare(InsertAntenatalCare):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
