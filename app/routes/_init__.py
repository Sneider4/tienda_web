from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import carrito_routes, categoria_routes, detalle_orden_routes, envio_routes,orden_routes, pago_routes, producto_routes, usuario_routes
