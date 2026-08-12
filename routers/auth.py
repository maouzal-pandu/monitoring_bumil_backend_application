from datetime import UTC, datetime, timedelta, timezone
import secrets
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from config import get_db
from core import PasswordHelper, generate_otp, otp, otp_expiry, send_otp_email
from schemas import (
    RegistSchema,
    VerifyOtpSchema,
    LoginSchema,
    ResetPasswordSchema,
    ForgotPasswordSchema,
)
from models import User, Desa, VerifyOtp, Kehamilan

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

    await send_otp_email(new_user.email, new_user.nama, otp_code)

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


@router.post("/verify-reset-password-otp")
def verify_otp_reset_password(payload: VerifyOtpSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    otp = (
        db.query(VerifyOtp)
        .filter(
            VerifyOtp.email == payload.email,
            VerifyOtp.otp == payload.code,
            VerifyOtp.is_used == False,
            VerifyOtp.tujuan == "reset_password",
        )
        .order_by(VerifyOtp.created_at.desc())
        .first()
    )

    if not user or not otp:
        raise HTTPException(status_code=400, detail="OTP tidak valid")

    if otp.expired_at < datetime.now():
        raise HTTPException(status_code=400, detail="OTP telah kadaluwarsa")

    otp.is_used = True
    if not user.is_verified:
        user.is_verified = True

    reset_token = secrets.token_urlsafe(32)
    otp.reset_token = reset_token  # atau simpan di tabel VerifyOtp/PasswordReset
    otp.reset_token_expires_at = datetime.now() + timedelta(minutes=10)

    db.commit()

    return {"reset_token": reset_token}


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            or_(
                User.nik == payload.identifier,
                User.nomer_telepon == payload.identifier,
                User.email == payload.identifier,
            )
        )
        .first()
    )

    if not user or not PasswordHelper.verify(payload.password, user.password):
        raise HTTPException(
            status_code=404, detail="Kredensial salah, silahkan coba lagi"
        )

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User belum terverifikasi")

    if user.role == "bumil":
        kehamilan = (
            db.query(Kehamilan)
            .filter(
                Kehamilan.user_id == user.id,
                Kehamilan.status_kehamilan == "berlangsung",
            )
            .first()
        )

        return {
            "user": user,
            "has_kehamilan": kehamilan is not None,
            "kehamilan": kehamilan,
        }

    return {"user": user}


@router.post("/send-reset-password-otp")
async def send_email(payload: ForgotPasswordSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if user is not None:
        otp_code = generate_otp()
        otp = VerifyOtp(
            email=user.email,
            otp=otp_code,
            expired_at=otp_expiry(),
            tujuan="reset_password",
        )

        db.add(otp)
        db.commit()

        await send_otp_email(to_email=user.email, nama=user.nama, otp_code=otp_code)

    return {"message": "Kode OTP telah terkirim, silahkan cek email"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    otp = (
        db.query(VerifyOtp)
        .filter(
            VerifyOtp.reset_token == payload.reset_token,
            VerifyOtp.reset_token_expires_at > datetime.now(),
        )
        .first()
    )
    if not otp:
        raise HTTPException(status_code=400, detail="Token tidak valid atau kadaluarsa")

    user = db.query(User).filter(User.email == otp.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Token tidak valid atau kadaluarsa")

    user.password = PasswordHelper.hash(payload.password)
    otp.reset_token = None
    db.commit()
    return {"message": "Password berhasil direset"}
