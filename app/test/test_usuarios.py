from app import create_app, db
import pytest
from io import BytesIO
from app.models.usuario import Usuario

#def test_login_usuario(client, usuario):
    # response = client.post('/usuario/login', data={
    #     'correo_electronico': usuario.correo_electronico,
    #     'contrasena': usuario.contrasena,
    # }, follow_redirects=True)
    # assert response.status_code == 200
    # assert b"Iniciar sesion" in response.data  


def test_delete_usuario(client, usuario):

    


    print(f"id user {usuario.id} nombre {usuario.nombre}")
    assert db.session.get(Usuario, usuario.id) is not None
    response = client.post(f'/usuario/delete/{usuario.id}', follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b"Usuario" in response.data 
    assert db.session.get(Usuario, usuario.id) is None