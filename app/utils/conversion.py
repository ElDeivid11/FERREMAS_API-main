import requests
from fastapi import HTTPException

def convertir_moneda(from_currency: str, to_currency: str, amount: float):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Validar 'result' solo si existe
        if "result" in data and data["result"] != "success":
            raise HTTPException(status_code=500, detail="Error en la respuesta de la API de tipo de cambio")

        rates = data.get("rates", {})
        if to_currency not in rates:
            raise HTTPException(status_code=400, detail=f"Moneda destino '{to_currency}' no encontrada")

        tipo_cambio = float(rates[to_currency])
        resultado = amount * tipo_cambio
        return {
            "converted_amount": round(resultado, 4),  # redondea
            "exchange_rate": tipo_cambio,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipo de cambio: {e}")
