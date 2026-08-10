from config.database import Base
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    DateTime,
    Enum,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, index=True, primary_key=True)
    nama = Column(String(100), nullable=False)
    nik = Column(String(25), nullable=False, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    nomer_telepon = Column(String(25), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    alamat = Column(Text)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    tanggal_lahir = Column(Date, nullable=False)
    role = Column(Enum("admin", "bidan", "bumil", name="role_enum"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
