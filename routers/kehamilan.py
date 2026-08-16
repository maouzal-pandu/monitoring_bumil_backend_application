from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from schemas import (
    SetHphtSchema,
    SetAntenatalCareSchedule,
    ChangeAncScheduleStatus,
)
from models import User, Kehamilan, ScheduleAnc, StatusJadwalAnc

router = APIRouter()


@router.post("/set-hpht")
def set_hpht(payload: SetHphtSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()

    if user is None:
        raise HTTPException(404, "User tidak ditemukan")

    kehamilan = (
        db.query(Kehamilan)
        .filter(
            Kehamilan.user_id == payload.user_id, Kehamilan.status_kehamilan == "aktif"
        )
        .first()
    )

    if kehamilan is None:
        kehamilan = Kehamilan(
            user_id=payload.user_id,
            hpht=payload.hpht,
            bb_awal=payload.bb_awal,
            gravida=payload.gravida,
            paritas=payload.paritas,
            abortus=payload.abortus,
            status_kehamilan="berlangsung",
        )
        db.add(kehamilan)
    else:
        kehamilan.hpht = payload.hpht

    db.commit()
    db.refresh(kehamilan)

    return {
        "message": "HPHT berhasil disimpan",
        "kehamilan": kehamilan,
    }


@router.post("/set-jadwal-anc")
def setAntenatalCareSchedule(
    payload: SetAntenatalCareSchedule, db: Session = Depends(get_db)
):
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


@router.post("/change-jadwal-anc-status")
def changeScheduleAncStatus(
    payload: ChangeAncScheduleStatus, db: Session = Depends(get_db)
):
    schedule_anc = (
        db.query(ScheduleAnc).filter(ScheduleAnc.id == payload.schedule_id).first()
    )

    if schedule_anc is None:
        raise HTTPException(404, "Id jadwal anc tidak ditemukan")

    schedule_anc.status = payload.status
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
