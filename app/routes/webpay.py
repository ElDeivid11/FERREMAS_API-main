# app/routes/webpay.py
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import traceback

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes

from app.database.db import get_db
from app.models.producto import Producto

router = APIRouter()

options = WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)
tx = Transaction(options)

@router.post("/webpay/crear")
async def crear_transaccion(request: Request):
    data = await request.json()
    buy_order = data.get("buy_order")
    session_id = str(buy_order) 
    amount = data.get("amount")
    return_url = str(request.url_for('retorno_webpay'))

    try:
        response = tx.create(buy_order, session_id, amount, return_url)
        # --- CORRECCIÓN FINAL ---
        # La respuesta es un diccionario. Se accede a los valores con ['clave'].
        return {"token": response['token'], "url": response['url']}
    except Exception as e:
        print("\n--- ERROR DETALLADO EN /webpay/crear ---")
        traceback.print_exc()
        print("----------------------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error al crear transacción: {e}")

@router.get("/webpay/retorno", response_class=HTMLResponse, name="retorno_webpay")
async def retorno_webpay(token_ws: str, db: Session = Depends(get_db)):
    try:
        response = tx.commit(token=token_ws)
        
        # --- CORRECCIÓN FINAL ---
        # La respuesta es un diccionario. Usamos .get('clave') para acceder a los valores.
        if response.get('status') == 'AUTHORIZED':
            codigo_producto = response.get('buy_order')
            producto_db = db.query(Producto).filter(Producto.codigo == codigo_producto).first()
            
            if producto_db is not None:
                if producto_db.stock > 0:  # type: ignore
                    producto_db.stock -= 1  # type: ignore
                    db.commit()
                    
                    detalle_html = f"<h1>Pago Aprobado</h1>"
                    detalle_html += f"<p><strong>Orden de Compra:</strong> {response.get('buy_order')}</p>"
                    detalle_html += f"<p><strong>Monto:</strong> ${response.get('amount')}</p>"
                    detalle_html += f"<p><strong>Producto:</strong> {producto_db.nombre}</p>"
                    detalle_html += f"<p>¡Gracias por tu compra!</p>"
                    return HTMLResponse(content=detalle_html)

            return HTMLResponse("<h1>Error</h1><p>El producto no se encontró o no hay stock.</p>", status_code=404)
        else:
            return HTMLResponse(f"<h1>Pago Rechazado</h1><p>Status: {response.get('status')}</p>", status_code=400)
    except Exception as e:
        print("\n--- ERROR DETALLADO EN /webpay/retorno ---")
        traceback.print_exc()
        print("------------------------------------------\n")
        raise HTTPException(status_code=500, detail=f"Error al procesar retorno: {e}")