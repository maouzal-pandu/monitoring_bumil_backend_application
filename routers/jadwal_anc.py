from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from models.kehamilan import Kehamilan
from models.schedule_anc import ScheduleAnc, StatusJadwalAnc
from schemas.jadwal_anc import (
    CancelScheduleSchema,
    EditScheduleSchema,
    SetScheduleSchema,
)

router = APIRouter()


@router.post("/set-jadwal-anc")
def setAntenatalCareSchedule(payload: SetScheduleSchema, db: Session = Depends(get_db)):
    kehamilan = db.query(Kehamilan).filter(Kehamilan.id == payload.kehamilan_id).first()

    if kehamilan is None:
        raise HTTPException(status_code=404, detail="ID kehamilan tidak ditemukan")

    if payload.tanggal_jadwal < date.today():
        raise HTTPException(400, "Tanggal jadwal tidak valid")

    schedule_anc = ScheduleAnc(
        kehamilan_id=payload.kehamilan_id,
        tanggal_jadwal=payload.tanggal_jadwal,
        catatan=payload.catatan,
    )

    db.add(schedule_anc)
    db.commit()
    db.refresh(schedule_anc)

    return {"message": "Berhasil mengatur jadwal anc"}


@router.post("/cancel-jadwal-anc")
def changeScheduleAncStatus(
    payload: CancelScheduleSchema, db: Session = Depends(get_db)
):
    schedule_anc = (
        db.query(ScheduleAnc).filter(ScheduleAnc.id == payload.schedule_id).first()
    )

    if schedule_anc is None:
        raise HTTPException(404, "Id jadwal anc tidak ditemukan")

    schedule_anc.status = StatusJadwalAnc.dibatalkan
    db.add(schedule_anc)
    db.commit()

    return {"message": "Berhasil membatalkan jadwal anc"}


@router.get("/jadwal-anc/{kehamilan_id}")
def getAntenatalCareSchedule(kehamilan_id: int, db: Session = Depends(get_db)):
    kehamilan = db.query(Kehamilan).filter(Kehamilan.id == kehamilan_id).first()

    if kehamilan is None:
        raise HTTPException(404, "ID kehamilan tidak ditemukan")

    schedule_anc = (
        db.query(ScheduleAnc)
        .filter(ScheduleAnc.kehamilan_id == kehamilan_id)
        .order_by(ScheduleAnc.tanggal_jadwal)
        .all()
    )

    return schedule_anc


@router.post("/edit-jadwal-anc")
def editAntenetalCareSchedule(
    payload: EditScheduleSchema, db: Session = Depends(get_db)
):
    schedule = db.query(ScheduleAnc).filter(ScheduleAnc.id == payload.id).first()

    if schedule is None:
        raise HTTPException(404, "Id tidak ditemukan")

    schedule.tanggal_jadwal = payload.tanggal
    schedule.catatan = payload.catatan

    db.commit()

    return {"message": "Berhasil mengubah jadwal"}
