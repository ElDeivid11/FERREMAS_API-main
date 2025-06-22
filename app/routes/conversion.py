from fastapi import APIRouter, Query
from app.utils.conversion import convertir_moneda  # Importas la función desde utils

router = APIRouter()

@router.get("/convertir")
def api_convertir_moneda(
    from_currency: str = Query(...),
    to_currency: str = Query(...),
    amount: float = Query(...)
):
    return convertir_moneda(from_currency, to_currency, amount)
