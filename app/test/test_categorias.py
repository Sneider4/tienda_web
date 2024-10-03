import pytest
from bs4 import BeautifulSoup
from app import db

@pytest.fixture
def usuarioc():
    return {
        'correo_electronico': 'test@example.com',
        'contrasena': 'password123',
        'rol' : 'Administrador'
    }

def test_login_usuario(client, usuarioc):
    # Obtener el token CSRF
    response = client.get('/usuario/login')
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    # Incluir el token CSRF en la solicitud POST
    response = client.post('/usuario/login', data={
        'correo_electronico': usuarioc['correo_electronico'],
        'contrasena': usuarioc['contrasena'],
        'csrf_token': csrf_token
    }, follow_redirects=True)
    assert response.status_code == 200, f"Error: {response.data.decode('utf-8')}"
    assert b"Iniciar sesion" in response.data


def test_index(client, user):

    response = client.get('/usuario/login', follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    response = client.post('/usuario/login', data={
        'csrf_token': csrf_token,
        'correo_electronico': user.correo_electronico,
        'contrasena': user.contrasena,
    }, follow_redirects=True)  

    response = client.get('/categorias', follow_redirects=True)

    assert response.status_code == 200
    assert "categ" in response.data.decode('utf-8')

def test_add_categoria(client, user):

    response = client.get('/usuario/login', follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    response = client.post('/usuario/login', data={
        'csrf_token': csrf_token,
        'correo_electronico': user.correo_electronico,
        'contrasena': user.contrasena,
    }, follow_redirects=True)  

    response = client.post('/categoria/add', data={
        'nombre': 'new_nombre',
        'descripcion': 'new_descripcion'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Categorias" in response.data

# def test_delete_categoria(client, categoria):
#     response = client.get(f'/categoria/delete/{categoria.id}', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Categorias" in response.data

# def test_edit_categoria(client, categoria):
#     response = client.post(f'/categoria/edit/{categoria.id}', data={
#         'nombre': 'updated_nombre',
#         'descripcion': 'updated_descripcion'
#     }, follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Guardar cambios" in response.data


