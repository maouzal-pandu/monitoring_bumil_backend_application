from datetime import date
from decimal import Decimal
from pydantic import BaseModel, condecimal
from models import StatusJadwalAnc


class SetHphtSchema(BaseModel):
    user_id: int
    hpht: date
    bb_awal: Decimal
    gravida: int
    paritas: int
    abortus: int


class SetAntenatalCareSchedule(BaseModel):
    kehamilan_id: int
    tanggal_jadwal: date
    catatan: str


class ChangeAncScheduleStatus(BaseModel):
    schedule_id: int
    status: StatusJadwalAnc
