from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class Desa(Base):
    __tablename__ = "desa"

    id = Column(Integer, primary_key=True)
    nama = Column(String(255))

    user_list = relationship("User", back_populates="desa")
