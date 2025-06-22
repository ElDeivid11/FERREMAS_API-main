import pytest
from pydantic import ValidationError
from unittest.mock import patch
from fastapi import HTTPException
from typing import Any

# Importamos las clases y funciones que vamos a probar
from app.schemas.producto_schema import ProductoSchema
from app.schemas.contacto_schema import ContactoSchema
from app.models.producto import Producto
from app.models.contacto import Contacto
from app.utils.conversion import convertir_moneda

# --- Pruebas para el Módulo de Conversión de Moneda (5 Pruebas) ---
@patch('app.utils.conversion.requests.get')
def test_convertir_clp_a_usd(mock_get):
    """Prueba 1: Verifica la conversión correcta de CLP a USD."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success", "rates": {"USD": 0.0011}}
    resultado = convertir_moneda("CLP", "USD", 1000)
    assert resultado["converted_amount"] == 1.1

@patch('app.utils.conversion.requests.get')
def test_convertir_monto_cero(mock_get):
    """Prueba 2: Verifica que al convertir un monto de 0, el resultado sea 0."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success", "rates": {"USD": 0.0011}}
    resultado = convertir_moneda("CLP", "USD", 0)
    assert resultado["converted_amount"] == 0

@patch('app.utils.conversion.requests.get')
def test_no_convertir_misma_moneda(mock_get):
    """Prueba 3: Verifica que si la moneda de origen y destino es la misma, el monto no cambia."""
    resultado = convertir_moneda("CLP", "CLP", 12345)
    assert resultado["converted_amount"] == 12345

@patch('app.utils.conversion.requests.get')
def test_conversion_moneda_invalida(mock_get):
    """Prueba 4: Verifica que la función lance una excepción con una moneda inexistente."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success", "rates": {"USD": 0.0011}}
    with pytest.raises(HTTPException):
        convertir_moneda("CLP", "XYZ", 1000)

@patch('app.utils.conversion.requests.get')
def test_tipo_de_retorno_conversion(mock_get):
    """Prueba 5: Verifica que la función siempre devuelva un diccionario con las claves esperadas."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": "success", "rates": {"USD": 0.0011}}
    resultado = convertir_moneda("CLP", "USD", 100)
    assert isinstance(resultado, dict)
    assert "converted_amount" in resultado

# --- Pruebas para los Esquemas y Modelos de Datos (5 Pruebas) ---

def test_creacion_producto_schema_valido():
    """Prueba 6: Verifica que se puede crear un ProductoSchema con datos válidos."""
    producto_data: dict[str, Any] = {"codigo": "P001", "marca": "MarcaX", "nombre": "Producto 1", "modelo": "M01", "stock": 100, "precio": 19990}
    producto = ProductoSchema(**producto_data)
    assert producto.codigo == "P001"

def test_creacion_producto_schema_invalido():
    """Prueba 7: Verifica que Pydantic lance un error si los tipos de datos son incorrectos."""
    with pytest.raises(ValidationError):
        ProductoSchema(codigo="P002", marca="MarcaY", nombre="Producto 2", stock="mucho", precio="caro") # type: ignore

def test_creacion_modelo_sqlalchemy_desde_schema():
    """Prueba 8: Verifica que el modelo de SQLAlchemy se pueda instanciar desde un esquema."""
    producto_schema = ProductoSchema(codigo="P003", marca="MarcaZ", nombre="Producto 3", modelo="M03", stock=50, precio=9990)
    db_producto = Producto(**producto_schema.model_dump())
    assert db_producto.codigo == "P003" # type: ignore

# En test_unitarios.py

def test_nombre_de_tabla_contacto():
    """Prueba 9: Verifica que el nombre de la tabla en el modelo Contacto sea el correcto."""
    assert Contacto.__tablename__ == 'contacto'

def test_contacto_schema_email_invalido():
    """Prueba 10: Verifica que Pydantic rechace un formato de email inválido."""
    with pytest.raises(ValidationError):
        ContactoSchema(nombre="test", correo="email-invalido", asunto="test", mensaje="test")