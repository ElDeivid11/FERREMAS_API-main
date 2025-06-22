from app.database.db import SessionLocal
from app.models.producto import Producto

db = SessionLocal()

producto1 = Producto(
    codigo="A123",
    nombre="Martillo",
    marca="Truper",
    modelo="M2020",
    stock=20,
    precio=5990
)

producto2 = Producto(
    codigo="B456",
    nombre="Taladro",
    marca="Bosch",
    modelo="X500",
    stock=10,
    precio=42990
)

db.add_all([producto1, producto2])
db.commit()
db.close()
