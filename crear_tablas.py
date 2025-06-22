from app.database.db import Base, engine
from app.models import producto, contacto  # 👈 importa ambos modelos

Base.metadata.create_all(bind=engine)
