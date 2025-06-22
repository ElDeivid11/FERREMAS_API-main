from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from app.schemas.contacto_schema import ContactoSchema
from app.models.contacto import Contacto as ContactoModel
from app.database.db import get_db

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

router = APIRouter()

@router.post("/contacto", tags=["Contacto"])
def enviar_correo_contacto(contacto: ContactoSchema, db: Session = Depends(get_db)):
    # --- Guardar el contacto en la base de datos ---
    db_contacto = ContactoModel(**contacto.model_dump())
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)

    # --- Leer credenciales de forma segura ---
    smtp_user = os.getenv("EMAIL_USER")
    smtp_password = os.getenv("EMAIL_PASS")

    if not smtp_user or not smtp_password:
        raise HTTPException(status_code=500, detail="Error de configuración del servidor de correo.")

    # === CORREO 1: Notificación para Ferremas ===
    msg_para_ferremas = MIMEMultipart()
    msg_para_ferremas['From'] = smtp_user
    msg_para_ferremas['To'] = smtp_user  # Se envía a tu propio correo
    msg_para_ferremas['Subject'] = f"Nuevo Mensaje de Contacto: {contacto.asunto}"
    
    cuerpo_mensaje_ferremas = f"""
    Has recibido un nuevo mensaje desde el formulario de contacto de tu tienda.

    Nombre: {contacto.nombre}
    Correo: {contacto.correo}
    Asunto: {contacto.asunto}

    Mensaje:
    {contacto.mensaje}
    """
    msg_para_ferremas.attach(MIMEText(cuerpo_mensaje_ferremas, 'plain'))


    # === CORREO 2: Confirmación para el Cliente ===
    msg_para_cliente = MIMEMultipart()
    msg_para_cliente['From'] = smtp_user
    msg_para_cliente['To'] = contacto.correo  # Se envía al correo del cliente
    msg_para_cliente['Subject'] = "Hemos recibido tu mensaje - Ferremas"

    cuerpo_mensaje_cliente = f"""
    Hola {contacto.nombre},

    ¡Gracias por ponerte en contacto con Ferremas!

    Hemos recibido tu mensaje y te responderemos a la brevedad posible.

    Este es un correo de confirmación automático, por favor no respondas a este mensaje.

    --- Resumen de tu consulta ---
    Asunto: {contacto.asunto}
    Mensaje: {contacto.mensaje}
    -----------------------------

    Atentamente,
    El equipo de Ferremas
    """
    msg_para_cliente.attach(MIMEText(cuerpo_mensaje_cliente, 'plain'))


    # --- Lógica de Envío de Correos ---
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        # Enviar ambos correos en la misma sesión
        server.sendmail(smtp_user, msg_para_ferremas['To'], msg_para_ferremas.as_string())
        server.sendmail(smtp_user, msg_para_cliente['To'], msg_para_cliente.as_string())
        
        server.quit()
        
        return {"message": "Mensaje enviado y confirmación remitida exitosamente"}

    except Exception as e:
        print(f"Error al enviar correo: {e}")
        raise HTTPException(status_code=500, detail="Hubo un error al intentar enviar el correo.")