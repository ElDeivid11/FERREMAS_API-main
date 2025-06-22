# En app/utils/conversion.py

import requests
from fastapi import HTTPException

def convertir_moneda(from_currency: str, to_currency: str, amount: float):
    # --- LÓGICA AÑADIDA ---
    # Si las monedas son iguales, no es necesario hacer la conversión.
    if from_currency == to_currency:
        return {
            "converted_amount": amount,
            "exchange_rate": 1.0,
            "original_amount": amount
        }
    # -------------------------

    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al contactar el servicio de conversión de moneda")
    
    data = response.json()
    if data.get("result") == "error":
        raise HTTPException(status_code=400, detail=data.get("error-type", "Error desconocido de la API de moneda"))

    rates = data.get("rates", {})
    if to_currency not in rates:
        raise HTTPException(status_code=400, detail=f"Moneda destino '{to_currency}' no encontrada")
    
    exchange_rate = rates[to_currency]
    converted_amount = round(amount * exchange_rate, 2)
    
    return {
        "converted_amount": converted_amount,
        "exchange_rate": exchange_rate,
        "original_amount": amount
    }