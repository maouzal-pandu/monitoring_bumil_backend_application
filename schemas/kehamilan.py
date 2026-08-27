from datetime import date
from decimal import Decimal
import decimal
import enum
from pydantic import BaseModel, condecimal
from sqlalchemy import Enum
from models import StatusJadwalAnc
from models.kehamilan import StatusRisiko


class SetHphtSchema(BaseModel):
    user_id: int
    hpht: date
    bb_awal: Decimal
    gravida: int
    paritas: int
    abortus: int


class KehamilanDetailResponse(BaseModel):
    id: int
    user_id: int
    nama_bumil: str
    tanggal_lahir: date
    nik: str
    nomer_telepon: str
    alamat: str
    latitude: Decimal
    longitude: Decimal
    tanggal_hpht: date
    status_risiko: StatusRisiko
    nama_desa: str
