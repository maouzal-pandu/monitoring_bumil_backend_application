from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from models.wilayah import Desa
from schemas import (
    SetHphtSchema,
    SetScheduleSchema,
    CancelScheduleSchema,
    EditScheduleSchema,
)
from models import User, Kehamilan, ScheduleAnc, StatusJadwalAnc
from schemas.kehamilan import KehamilanDetailResponse

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


@router.get("/kehamilan")
def getKehamilan(db: Session = Depends(get_db), page: int = 1, limit: int = 10):
    skip = (page - 1) * limit

    total = db.query(Kehamilan).count()

    data = (
        db.query(
            Kehamilan.id,
            Kehamilan.hpht,
            Kehamilan.status_risiko,
            User.nama,
            User.nik,
        )
        .filter(Kehamilan.status_kehamilan == "berlangsung")
        .join(User, Kehamilan.user_id == User.id)
        .order_by(Kehamilan.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = [
        {
            "kehamilan_id": row.id,
            "hpht": row.hpht,
            "nama": row.nama,
            "nik": row.nik,
            "status_risiko": row.status_risiko,
        }
        for row in data
    ]

    return {
        "data": result,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/kehamilan/{kehamilan_id}", response_model=KehamilanDetailResponse)
def get_kehamilan_detail(kehamilan_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(
            Kehamilan.id,
            Kehamilan.user_id,
            User.nama.label("nama_bumil"),
            User.nik,
            User.nomer_telepon,
            User.alamat,
            User.latitude,
            User.longitude,
            User.tanggal_lahir,
            Kehamilan.hpht,
            Kehamilan.status_risiko,
            Desa.nama.label("nama_desa"),
        )
        .join(User, Kehamilan.user_id == User.id)
        .outerjoin(Desa, User.desa_id == Desa.id)
        .filter(Kehamilan.id == kehamilan_id)
        .first()
    )

    if row is None:
        raise HTTPException(status_code=404, detail="Data kehamilan tidak ditemukan")

    return {
        "id": row.id,
        "user_id": row.user_id,
        "nama_bumil": row.nama_bumil,
        "tanggal_lahir": row.tanggal_lahir,
        "nik": row.nik,
        "nomer_telepon": row.nomer_telepon,
        "alamat": row.alamat,
        "latitude": row.latitude,
        "longitude": row.longitude,
        "tanggal_hpht": row.hpht,
        "status_risiko": row.status_risiko,
        "nama_desa": row.nama_desa,
    }
