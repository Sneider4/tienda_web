from app import create_app, db
import pytest
from app.models.usuario import Usuario

@pytest.fixture
def app():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def usuario(app):
    usuario = Usuario(
        nombre="test_user", 
        apellido="test_apellido",
        correo_electronico="test_user@example.com",
        telefono="test_telefono",
        contrasena="test_contrasena",
        departamento="test_departamento",
        ciudad="test_ciudad",
        genero="test_genero",
        fecha_nacimiento="2000-01-01",
        imagen="test_imagen"
    )
    db.session.add(usuario)
    db.session.commit()
    yield usuario
    db.session.delete(usuario)