from datetime import date

from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class RoleEnum(str, Enum):
    bumil = "bumil"
    admin = "admin"
    bidan = "bidan"


class PurposeEnum(str, Enum):
    regist = "regist"
    reset_password = "reset_password"


class RegistSchema(BaseModel):
    nama: str
    nik: str
    email: str
    nomer_telepon: str
    password: str
    alamat: str
    desa_id: int
    latitude: float
    longitude: float
    tanggal_lahir: date
    role: RoleEnum


class LoginSchema(BaseModel):
    identifier: str  # Email/Nomer Telepon/NIK
    password: str


class VerifyOtpSchema(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    reset_token: str
    password: str


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
