from datetime import date

from pydantic import BaseModel


class SetScheduleSchema(BaseModel):
    kehamilan_id: int
    tanggal_jadwal: date
    catatan: str


class CancelScheduleSchema(BaseModel):
    schedule_id: int


class EditScheduleSchema(BaseModel):
    id: int
    tanggal: date
    catatan: str
