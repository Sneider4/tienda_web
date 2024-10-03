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
    usuario = Usuario(nombre="test_user", contrasena="test_contrasena" )
    db.session.add(usuario)
    db.session.commit
    yield usuario

@pytest.fixture
def categoria(app):
    from app.models.categoria import Categoria
    categoria = Categoria(nombre="test_categoria", descripcion="test_descripcion" )
    db.session.add(categoria)
    db.session.commit
    yield categoria