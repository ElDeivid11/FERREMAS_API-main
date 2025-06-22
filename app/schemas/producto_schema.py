# app/schemas/producto_schema.py
from pydantic import BaseModel
from typing import Optional

class ProductoSchema(BaseModel):
    codigo: str
    marca: str
    nombre: str
    modelo: str
    stock: int
    precio: int # <--- AÑADIR ESTA LÍNEA
    imagen_url: Optional[str] = None # <--- AÑADIR ESTA LÍNEA

    class Config:
        from_attributes = True # <--- CAMBIAR ESTA LÍNEA