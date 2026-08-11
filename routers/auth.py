from datetime import UTC, datetime, timezone
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config import get_db
from core import PasswordHelper, generate_otp, otp_expiry, send_otp_email
from schemas import RegistSchema, VerifyOtpSchema
from models import User, Desa, VerifyOtp

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegistSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    if db.query(User).filter(User.nik == payload.nik).first():
        raise HTTPException(status_code=400, detail="NIK sudah terdaftar")

    if db.query(User).filter(User.nomer_telepon == payload.nomer_telepon).first():
        raise HTTPException(status_code=400, detail="Nomor telepon sudah terdaftar")

    desa = db.query(Desa).filter(Desa.id == payload.desa_id).first()
    if not desa:
        raise HTTPException(status_code=404, detail="Desa tidak ditemukan")

    hashed_password = PasswordHelper.hash(payload.password)

    new_user = User(
        nama=payload.nama,
        nik=payload.nik,
        email=payload.email,
        nomer_telepon=payload.nomer_telepon,
        password=hashed_password,
        alamat=payload.alamat,
        desa_id=payload.desa_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        tanggal_lahir=payload.tanggal_lahir,
        role=payload.role.value,
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    otp_code = generate_otp()
    otp_exp = otp_expiry()
    otp = VerifyOtp(
        email=new_user.email, otp=otp_code, expired_at=otp_exp, tujuan="registrasi"
    )

    db.add(otp)
    db.commit()

    await send_otp_email(cast(str, new_user.email), cast(str, new_user.nama), otp_code)

    return {
        "message": "Registrasi berhasil, silahkan cek email untuk kode otp",
    }


@router.post("/verify-regist-otp")
def verify_otp_regist(payload: VerifyOtpSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    otp = (
        db.query(VerifyOtp)
        .filter(
            VerifyOtp.email == payload.email,
            VerifyOtp.otp == payload.code,
            VerifyOtp.is_used == False,
            VerifyOtp.tujuan == "registrasi",
        )
        .order_by(VerifyOtp.created_at.desc())
        .first()
    )

    if not otp:
        raise HTTPException(status_code=400, detail="OTP tidak valid")

    if otp.expired_at < datetime.now():
        raise HTTPException(status_code=404, detail="OTP telah kadaluwarsa")

    otp.is_used = True
    user.is_verified = True
    db.commit()

    return {"message": "Akun berhasil diverifikasi"}
