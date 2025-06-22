from app.database.db import Base, engine
from app.models.producto import Producto

Base.metadata.create_all(bind=engine)