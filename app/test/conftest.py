from app import create_app, db
import pytest

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        #db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    from app.models.usuario import Usuario
    usuario = Usuario(nombre="test_user", apellido="test_apellido", correo_electronico="testscorreo@gmail.com", 
                      telefono="1234567891", departamento= "test_departamento", ciudad="test_ciudad", 
                      genero="test_genero", contrasena="test_contrasena", fecha_nacimiento="2024-07-08", 
                      rol="Administrador", imagen="test_imagen")
    db.session.add(usuario)
    db.session.commit
    yield usuario
    # db.session.delete(usuario)
    # db.session.commit()
