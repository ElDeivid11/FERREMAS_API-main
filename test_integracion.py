from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import os

client = TestClient(app)
test_product_code = "TEST_INT_01"

def test_1_crear_producto_integracion():
    """Prueba 1: POST /productos - Verifica que un producto pueda ser creado."""
    response = client.post(
        "/productos/",
        json={"codigo": test_product_code, "marca": "MarcaIntegracion", "nombre": "Producto de Integracion", "modelo": "TI-01", "stock": 50, "precio": 10000}
    )
    assert response.status_code == 201
    assert response.json()["codigo"] == test_product_code

def test_2_listar_productos_integracion():
    """Prueba 2: GET /productos - Verifica que la API devuelva una lista de productos."""
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_3_obtener_producto_existente():
    """Prueba 3: GET /productos/{codigo} - Verifica que se pueda obtener un producto."""
    response = client.get(f"/productos/{test_product_code}")
    assert response.status_code == 200
    assert response.json()["codigo"] == test_product_code

def test_4_actualizar_producto_integracion():
    """Prueba 4: PUT /productos/{codigo} - Verifica que un producto pueda ser actualizado."""
    response = client.put(
        f"/productos/{test_product_code}",
        json={"codigo": test_product_code, "marca": "MarcaIntegracion", "nombre": "Producto Actualizado", "modelo": "TI-02", "stock": 40, "precio": 12000}
    )
    assert response.status_code == 200
    assert response.json()["stock"] == 40

def test_5_obtener_producto_inexistente():
    """Prueba 5: GET /productos/{codigo} - Verifica que devuelva 404 para un producto que no existe."""
    response = client.get("/productos/CODIGO_QUE_NO_EXISTE")
    assert response.status_code == 404

def test_6_integracion_subida_imagen():
    """Prueba 6: POST /{codigo}/upload-image/ - Verifica el flujo de subida de archivos."""
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake_image_content")
    
    with open("test_image.jpg", "rb") as f:
        response = client.post(f"/productos/{test_product_code}/upload-image/", files={"file": ("test_image.jpg", f, "image/jpeg")})
    
    os.remove("test_image.jpg") # Limpiar el archivo creado
    assert response.status_code == 200
    assert "imagen_url" in response.json()
    assert response.json()["imagen_url"] is not None

@patch('smtplib.SMTP')
def test_7_integracion_formulario_contacto(mock_smtp):
    """Prueba 7: POST /contacto - Verifica el flujo del formulario de contacto."""
    response = client.post("/contacto/", json={"nombre": "Cliente Integracion", "correo": "integracion@test.com", "asunto": "Test", "mensaje": "Mensaje"})
    assert response.status_code == 200
    assert "confirmación remitida" in response.json()["message"]

def test_8_integracion_webpay_crear():
    """Prueba 8: POST /webpay/crear - Verifica la integración con la SDK de Transbank."""
    response = client.post("/webpay/crear", json={"buy_order": "ORDEN_INTEGRACION", "amount": 9990})
    assert response.status_code == 200
    assert "token" in response.json()
    assert "url" in response.json()

def test_9_integracion_conversion_moneda_api_real():
    """Prueba 9: GET /api/convertir - Verifica la integración real con la API de conversión."""
    response = client.get("/api/convertir?from_currency=USD&to_currency=CLP&amount=10")
    assert response.status_code == 200
    assert "converted_amount" in response.json()

def test_10_eliminar_producto_integracion():
    """Prueba 10: DELETE /productos/{codigo} - Verifica que se pueda eliminar un producto."""
    response = client.delete(f"/productos/{test_product_code}")
    assert response.status_code == 204