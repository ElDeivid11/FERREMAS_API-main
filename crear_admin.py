from app.database.db import SessionLocal, engine, Base
from app.models.user import User
from app.utils.security import get_password_hash

# Crear tablas (incluida la nueva tabla de usuarios)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- IMPORTANTE: Define aquí tu usuario y contraseña de admin ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Verificar si el usuario ya existe
db_user = db.query(User).filter(User.username == ADMIN_USERNAME).first()

if not db_user:
    hashed_password = get_password_hash(ADMIN_PASSWORD)
    new_user = User(username=ADMIN_USERNAME, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    print(f"Usuario '{ADMIN_USERNAME}' creado exitosamente.")
else:
    print(f"El usuario '{ADMIN_USERNAME}' ya existe.")

db.close()