from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from app.database.db import get_db
from app.models.producto import Producto
from app.schemas.producto_schema import ProductoSchema

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=list[ProductoSchema])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.post("/", response_model=ProductoSchema, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.post("/{codigo}/upload-image/", response_model=ProductoSchema)
def upload_image(codigo: str, db: Session = Depends(get_db), file: UploadFile = File(...)):
    producto = db.query(Producto).filter(Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not file.filename:
        raise HTTPException(status_code=400, detail="El archivo subido no tiene nombre.")
    
    file_extension = os.path.splitext(file.filename)[1]
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = f"static/uploads/{unique_filename}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    image_url = f"http://localhost:8000/{file_location}"
    
    # --- CORRECCIÓN APLICADA AQUÍ ---
    # Se añade # type: ignore para suprimir el falso positivo de Pylance
    producto.imagen_url = image_url  # type: ignore
    
    db.commit()
    db.refresh(producto)
    
    return producto

@router.get("/{codigo}", response_model=ProductoSchema)
def obtener_producto(codigo: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{codigo}", response_model=ProductoSchema)
def actualizar_producto(codigo: str, producto_actualizado: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.codigo == codigo).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in producto_actualizado.model_dump().items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(codigo: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return