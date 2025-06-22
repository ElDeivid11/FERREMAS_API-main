# app/models/producto.py
from sqlalchemy import Column, String, Integer
from app.database.db import Base

class Producto(Base):
    __tablename__ = "productos"

    codigo = Column(String(10), primary_key=True, index=True)
    marca = Column(String(50))
    nombre = Column(String(100))
    modelo = Column(String(50))
    stock = Column(Integer)
    precio = Column(Integer, nullable=False) # <--- AÑADIR ESTA LÍNEA
    imagen_url = Column(String(255), nullable=True)