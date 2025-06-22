import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importaciones de la aplicación
from app.database.db import Base, engine
from app.routes import productos, contacto, conversion, webpay

# --- Configuración Inicial ---
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

app = FastAPI(title="FERREMAS API")

# El middleware de CORS es crucial para que este método funcione
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite conexiones desde orígenes 'null' (file:///)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Inclusión de Rutas de la API
app.include_router(productos.router)
app.include_router(contacto.router)
app.include_router(conversion.router, prefix="/api")
app.include_router(webpay.router)

# Montaje de Directorios Estáticos
# Esto es solo para que las imágenes (logo y productos) sean accesibles vía URL
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"mensaje": "FERREMAS API funcionando. Las páginas HTML se abren directamente."}