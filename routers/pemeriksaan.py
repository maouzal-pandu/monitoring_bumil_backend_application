from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.pemeriksaan import Pemeriksaan
from schemas.pemeriksaan import (
    InsertAntenatalCare,
    UpdateAntenatalCare,
    ResponseAntenatalCare,
)

router = APIRouter()


@router.post("/insert-pemeriksaan", response_model=ResponseAntenatalCare)
def insertAntenatalCare(payload: InsertAntenatalCare, db: Session = Depends(get_db)):
    new_pemeriksaan = Pemeriksaan(**payload.model_dump())
    db.add(new_pemeriksaan)
    db.commit()
    db.refresh(new_pemeriksaan)
    return new_pemeriksaan


@router.get("/pemeriksaan/{kehamilan_id}", response_model=list[ResponseAntenatalCare])
def getPemeriksaanByKehamilan(kehamilan_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Pemeriksaan)
        .filter(Pemeriksaan.kehamilan_id == kehamilan_id)
        .order_by(Pemeriksaan.created_at.desc())
        .all()
    )


@router.get(
    "/pemeriksaan/detail/{pemeriksaan_id}", response_model=ResponseAntenatalCare
)
def getPemeriksaanById(pemeriksaan_id: int, db: Session = Depends(get_db)):
    data = db.query(Pemeriksaan).filter(Pemeriksaan.id == pemeriksaan_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")
    return data


@router.put(
    "/update-pemeriksaan/{pemeriksaan_id}", response_model=ResponseAntenatalCare
)
def updateAntenatalCare(
    pemeriksaan_id: int, payload: UpdateAntenatalCare, db: Session = Depends(get_db)
):
    data = db.query(Pemeriksaan).filter(Pemeriksaan.id == pemeriksaan_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(data, field, value)

    db.commit()
    db.refresh(data)
    return data


@router.delete("/delete-pemeriksaan/{pemeriksaan_id}")
def deleteAntenatalCare(pemeriksaan_id: int, db: Session = Depends(get_db)):
    data = db.query(Pemeriksaan).filter(Pemeriksaan.id == pemeriksaan_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")

    db.delete(data)
    db.commit()
    return {"message": "Pemeriksaan berhasil dihapus"}
