from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from schemas import SetHphtSchema
from models import User, Kehamilan

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
