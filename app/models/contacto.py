from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base

class Contacto(Base):
    __tablename__ = "contacto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    asunto = Column(String(150), nullable=False)
    mensaje = Column(Text, nullable=False)
