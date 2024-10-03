from app import create_app, db
import pytest
from io import BytesIO
from app.models.usuario import Usuario

# def test_add_usuario(client, usuario):
#     response = client.post('/usuario/add', data={
#         'nombre': 'new_nombre',
#         'apellido': 'new_apellido',
#         'correo_electronico': 'new_correo_electronico@gmail.com',
#         'telefono': 'new_telefono',
#         'contrasena': 'new_password',
#         'departamento': 'new_departamento',
#         'ciudad': 'new_ciudad',
#         'genero': 'new_genero',
#         'fecha_nacimiento': '2000-01-01',
#         'imagen': (BytesIO(b'mock_image_data'), 'test_image.jpg')

#     },content_type='multipart/form-data', follow_redirects=True)
#     assert response.status_code == 200


# def test_delete_usuario(client, usuario):
#     response = client.post(f'/usuario/delete/{usuario.id}', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"elminado" in response.data 
#     assert Usuario.query.get(usuario.id) is None


def test_login_usuario(client, usuario):
    response = client.post('/usuario/login', data={
        'correo_electronico': usuario.correo_electronico,
        'contrasena': usuario.contrasena,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Iniciar sesion" in response.data  
