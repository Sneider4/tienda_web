from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('config.Config')
    
    app.config['SECRET_KEY'] = os.urandom(24)
    
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'usuario.login'

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        from .models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    csrf.init_app(app)

    from app.routes import carrito_routes, categoria_routes, detalle_orden_routes, envio_routes,orden_routes, pago_routes, producto_routes, usuario_routes, admin_routes, direccion_cliente_routes

    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(detalle_orden_routes.bp)
    app.register_blueprint(envio_routes.bp)
    app.register_blueprint(orden_routes.bp)
    app.register_blueprint(pago_routes.bp)
    app.register_blueprint(producto_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(direccion_cliente_routes.bp)
    app.register_blueprint(admin_routes.bp)

    
    return app