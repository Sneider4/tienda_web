
def test_login_usuario(client, usuario):
    response = client.post('/usuario/login', data={
        'correo_electronico': usuario.correo_electronico,
        'contrasena': usuario.contrasena,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Iniciar sesion" in response.data

def test_index(client):
    response = client.get('/categoria', follow_redirects=True)
    assert response.status_code == 200
    assert b"Categorias" in response.data

# def test_add_categoria(client):
#     response = client.post('/categoria/add', data={
#         'nombre': 'new_nombre',
#         'descripcion': 'new_descripcion'
#     }, follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Categorias" in response.data

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


